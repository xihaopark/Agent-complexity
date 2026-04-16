"""Multimodal tools: read images and PDFs (local workspace)."""
from __future__ import annotations

import base64
import io
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Type

from PIL import Image
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool

_JPEG_QUALITY = 85
_MAX_IMAGE_DIM = 2048
_PDF_PAGE_THRESHOLD = 20

_SUPPORTED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".tiff", ".tif"}


@dataclass
class MultimodalToolResult:
    text: str = ""
    images: List[Dict[str, str]] = field(default_factory=list)

    def to_langchain_content(self) -> list:
        blocks = []
        if self.text:
            blocks.append({"type": "text", "text": self.text})
        for img in self.images:
            blocks.append({"type": "image", "base64": img["base64"], "mime_type": img["mime_type"]})
        return blocks or [{"type": "text", "text": "(empty result)"}]


def _encode_image(image_path: Path, max_dim: int = _MAX_IMAGE_DIM, jpeg_quality: int = _JPEG_QUALITY) -> Dict[str, str]:
    img = Image.open(image_path)
    w, h = img.size
    if max(w, h) > max_dim:
        scale = max_dim / max(w, h)
        img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
    has_alpha = img.mode in ("RGBA", "LA", "PA")
    if has_alpha:
        out_format, mime = "PNG", "image/png"
    else:
        if img.mode != "RGB":
            img = img.convert("RGB")
        out_format, mime = "JPEG", "image/jpeg"
    buf = io.BytesIO()
    img.save(buf, format=out_format, quality=jpeg_quality)
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    return {"base64": b64, "mime_type": mime}


def _encode_pdf_page_as_image(pdf_path: Path, page_no: int, dpi: int = 150, jpeg_quality: int = _JPEG_QUALITY) -> Dict[str, str]:
    import pymupdf
    doc = pymupdf.open(str(pdf_path))
    page = doc[page_no]
    zoom = dpi / 72.0
    mat = pymupdf.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    w, h = img.size
    if max(w, h) > _MAX_IMAGE_DIM:
        scale = _MAX_IMAGE_DIM / max(w, h)
        img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=jpeg_quality)
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    doc.close()
    return {"base64": b64, "mime_type": "image/jpeg"}


class ReadImageInput(BaseModel):
    image_path: str = Field(description="Path to the image file (relative to workspace).")


class ReadImageTool(BaseTool):
    name: str = "read_image"
    description: str = (
        "Read an image from the workspace for the LLM to analyse. "
        "Supported: jpg, png, gif, webp, bmp, tiff."
    )
    args_schema: Type[BaseModel] = ReadImageInput
    data_root: Optional[Path] = None

    def __init__(self, data_root: Path, **kwargs):
        super().__init__(**kwargs)
        self.data_root = Path(data_root).resolve()

    def _run(self, image_path: str) -> MultimodalToolResult:
        image_path = image_path.strip().strip("/")
        if ".." in image_path:
            return MultimodalToolResult(text=f"Error: '..' not allowed in path: {image_path}")
        full_path = self.data_root / image_path
        if not full_path.exists():
            return MultimodalToolResult(text=f"Error: file not found: {image_path}")
        if full_path.suffix.lower() not in _SUPPORTED_IMAGE_EXTENSIONS:
            return MultimodalToolResult(
                text=f"Error: unsupported image format. Supported: {', '.join(sorted(_SUPPORTED_IMAGE_EXTENSIONS))}"
            )
        try:
            img_data = _encode_image(full_path)
            img = Image.open(full_path)
            w, h = img.size
            size_kb = full_path.stat().st_size / 1024
            return MultimodalToolResult(
                text=f"Image loaded: {image_path} ({w}×{h} px, {size_kb:.0f} KB).",
                images=[img_data],
            )
        except Exception as e:
            return MultimodalToolResult(text=f"Error reading image {image_path}: {e}")


class ReadPdfInput(BaseModel):
    pdf_path: str = Field(description="Path to the PDF file (relative to workspace).")
    page_range: Optional[str] = Field(default=None, description="Optional page range, e.g. '1-5' or '3,7,10'.")
    search_query: Optional[str] = Field(default=None, description="Optional regex search for long PDFs.")


class ReadPdfTool(BaseTool):
    name: str = "read_pdf"
    description: str = (
        "Read a PDF from the workspace. Short PDFs (≤20 pages) as images; "
        "long ones as text. Use search_query (regex) for long PDFs. Supports page_range."
    )
    args_schema: Type[BaseModel] = ReadPdfInput
    data_root: Optional[Path] = None
    page_threshold: int = _PDF_PAGE_THRESHOLD

    def __init__(self, data_root: Path, page_threshold: int = _PDF_PAGE_THRESHOLD, **kwargs):
        super().__init__(**kwargs)
        self.data_root = Path(data_root).resolve()
        self.page_threshold = page_threshold

    def _run(
        self,
        pdf_path: str,
        page_range: Optional[str] = None,
        search_query: Optional[str] = None,
    ) -> MultimodalToolResult:
        pdf_path = pdf_path.strip().strip("/")
        if ".." in pdf_path:
            return MultimodalToolResult(text=f"Error: '..' not allowed in path: {pdf_path}")
        full_path = self.data_root / pdf_path
        if not full_path.exists():
            return MultimodalToolResult(text=f"Error: file not found: {pdf_path}")
        if full_path.suffix.lower() != ".pdf":
            return MultimodalToolResult(text=f"Error: not a PDF file: {pdf_path}")
        try:
            import pymupdf
            doc = pymupdf.open(str(full_path))
            total_pages = len(doc)
            doc.close()
        except Exception as e:
            return MultimodalToolResult(text=f"Error opening PDF: {e}")
        pages = self._parse_page_range(page_range, total_pages)
        effective_pages = len(pages) if pages is not None else total_pages
        use_images = effective_pages <= self.page_threshold
        if use_images:
            return self._read_as_images(full_path, pages, total_pages)
        return self._read_as_text(full_path, pages, total_pages, search_query)

    def _read_as_images(self, pdf_path: Path, pages: Optional[List[int]], total_pages: int) -> MultimodalToolResult:
        if pages is None:
            pages = list(range(total_pages))
        images = []
        errors = []
        for pg in pages:
            try:
                images.append(_encode_pdf_page_as_image(pdf_path, pg))
            except Exception as e:
                errors.append(f"Page {pg + 1}: {e}")
        text = f"PDF loaded as images: {pdf_path.name} ({len(images)}/{total_pages} pages)."
        if errors:
            text += f"\nErrors: {'; '.join(errors)}"
        return MultimodalToolResult(text=text, images=images)

    def _read_as_text(
        self,
        pdf_path: Path,
        pages: Optional[List[int]],
        total_pages: int,
        search_query: Optional[str],
    ) -> MultimodalToolResult:
        import pymupdf
        doc = pymupdf.open(str(pdf_path))
        if pages is None:
            pages = list(range(total_pages))
        page_texts = []
        for pg in pages:
            text = doc[pg].get_text("text")
            if text.strip():
                page_texts.append(f"--- Page {pg + 1} ---\n{text}")
        doc.close()
        full_text = "\n\n".join(page_texts)
        if search_query:
            matches = self._search_in_text(full_text, search_query)
            if matches:
                text_out = f"PDF search results for '{search_query}' in {pdf_path.name}:\n\n" + "\n\n---\n\n".join(matches)
            else:
                text_out = f"No matches for '{search_query}' in {pdf_path.name}."
        else:
            max_chars = 200_000
            if len(full_text) > max_chars:
                text_out = f"PDF text: {pdf_path.name} (truncated to {max_chars} chars).\n\n" + full_text[:max_chars] + "\n\n... [TRUNCATED]"
            else:
                text_out = f"PDF text: {pdf_path.name} ({total_pages} pages).\n\n" + full_text
        return MultimodalToolResult(text=text_out)

    @staticmethod
    def _search_in_text(full_text: str, query: str, context_chars: int = 500) -> List[str]:
        try:
            pattern = re.compile(query, re.IGNORECASE)
        except re.error:
            pattern = re.compile(re.escape(query), re.IGNORECASE)
        matches = []
        seen = []
        for m in pattern.finditer(full_text):
            start = max(0, m.start() - context_chars)
            end = min(len(full_text), m.end() + context_chars)
            if seen and start < seen[-1][1]:
                seen[-1] = (seen[-1][0], end)
                matches[-1] = full_text[seen[-1][0]:end]
            else:
                seen.append((start, end))
                matches.append(full_text[start:end])
            if len(matches) >= 20:
                break
        return matches

    @staticmethod
    def _parse_page_range(page_range: Optional[str], total_pages: int) -> Optional[List[int]]:
        if not page_range:
            return None
        pages = set()
        for part in page_range.split(","):
            part = part.strip()
            if "-" in part:
                try:
                    a, b = part.split("-", 1)
                    for p in range(max(1, int(a.strip())), min(total_pages, int(b.strip())) + 1):
                        pages.add(p - 1)
                except ValueError:
                    continue
            else:
                try:
                    p = int(part)
                    if 1 <= p <= total_pages:
                        pages.add(p - 1)
                except ValueError:
                    continue
        return sorted(pages) if pages else None
