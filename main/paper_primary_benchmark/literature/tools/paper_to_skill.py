#!/usr/bin/env python3
"""Generate a Cursor SKILL.md from a DOI (Crossref), PDF text (PyMuPDF), or plain text file."""

from __future__ import annotations

import argparse
import json
import re
import ssl
import sys
import urllib.parse
import urllib.request
from pathlib import Path


def _ssl_context() -> ssl.SSLContext:
    try:
        import certifi

        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()

_MAX_BODY_CHARS = 12000


def _slug_from_doi(doi: str) -> str:
    return re.sub(r"[^\w.+-]+", "-", doi.strip().lower()).strip("-")


def fetch_crossref(doi: str) -> dict[str, str]:
    url = f"https://api.crossref.org/works/{urllib.parse.quote(doi)}"
    req = urllib.request.Request(url, headers={"User-Agent": "Paper2Skills/paper_to_skill (mailto:)"})
    with urllib.request.urlopen(req, timeout=45, context=_ssl_context()) as r:
        data = json.loads(r.read().decode())["message"]
    title = ""
    if data.get("title"):
        title = data["title"][0]
    abstract = ""
    if data.get("abstract"):
        # JATS sometimes embedded
        raw = data["abstract"]
        if isinstance(raw, str):
            abstract = re.sub(r"<[^>]+>", "", raw)
    return {"title": title, "abstract": abstract.strip(), "doi": doi}


def extract_pdf_text(path: Path, max_pages: int = 8) -> str:
    try:
        import fitz  # PyMuPDF
    except ImportError as e:
        raise SystemExit(
            "PyMuPDF not installed. Run: pip install pymupdf\n"
            "Or use --doi / --text-file instead."
        ) from e
    doc = fitz.open(path)
    parts: list[str] = []
    for i in range(min(len(doc), max_pages)):
        parts.append(doc[i].get_text("text"))
    return "\n".join(parts)


def write_skill(
    *,
    out_dir: Path,
    name: str,
    description: str,
    body: str,
) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    skill_path = out_dir / "SKILL.md"
    if len(body) > _MAX_BODY_CHARS:
        body = body[:_MAX_BODY_CHARS] + "\n\n_(truncated)_\n"
    content = f"""---
name: {name}
description: >-
  {description}
---

# Paper-derived skill

{body}
"""
    skill_path.write_text(content, encoding="utf-8")
    return skill_path


def main() -> None:
    p = argparse.ArgumentParser(description="Create .cursor/skills/.../SKILL.md from paper sources")
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--doi", help="DOI; fills title/abstract via Crossref if no PDF/text")
    src.add_argument("--pdf", type=Path, help="Local PDF path (needs pymupdf)")
    src.add_argument("--text-file", type=Path, help="Plain text excerpt (e.g. from paperskills extract)")
    p.add_argument("--title", help="Override title when using --text-file")
    p.add_argument("--max-pages", type=int, default=8, help="PDF pages to read")
    p.add_argument(
        "--out-skill-dir",
        type=Path,
        required=True,
        help="e.g. .cursor/skills/paper-kallisto-nbt-3519",
    )
    args = p.parse_args()

    body_parts: list[str] = []
    title = args.title or "Paper-derived notes"
    desc = ""
    skill_name = ""

    if args.doi:
        meta = fetch_crossref(args.doi)
        title = meta["title"] or title
        skill_name = f"paper-{_slug_from_doi(args.doi)}"
        desc = (title[:220] + "…") if len(title) > 220 else title
        body_parts.append(f"## Source\n\n- DOI: `{args.doi}`\n")
        if meta["abstract"]:
            body_parts.append("## Abstract (Crossref)\n\n" + meta["abstract"] + "\n")
        else:
            body_parts.append(
                "_No abstract in Crossref record; add PDF with --pdf to this skill dir and re-run,_\n"
                "_or paste excerpts under ## Notes._\n"
            )
    elif args.pdf:
        if not args.pdf.is_file():
            print("ERROR: PDF not found:", args.pdf, file=sys.stderr)
            sys.exit(1)
        text = extract_pdf_text(args.pdf.resolve(), max_pages=args.max_pages)
        skill_name = _slug_from_doi(args.pdf.stem) if args.pdf.stem else "paper-from-pdf"
        skill_name = "paper-" + re.sub(r"[^\w-]+", "-", skill_name)[:80].strip("-")
        title = args.title or args.pdf.stem
        desc = f"Extracted notes from {args.pdf.name}"
        body_parts.append("## Extracted text (first pages)\n\n```\n" + text + "\n```\n")
    else:
        raw = args.text_file.read_text(encoding="utf-8", errors="replace")
        title = args.title or args.text_file.stem
        skill_name = "paper-" + re.sub(r"[^\w-]+", "-", title.lower())[:80].strip("-")
        desc = f"Notes from {args.text_file.name}"
        body_parts.append("## Source text\n\n" + raw + "\n")

    if not skill_name:
        skill_name = "paper-derived"

    out = write_skill(
        out_dir=args.out_skill_dir,
        name=skill_name,
        description=desc[:500],
        body="\n".join(body_parts),
    )
    print("Wrote:", out)


if __name__ == "__main__":
    main()
