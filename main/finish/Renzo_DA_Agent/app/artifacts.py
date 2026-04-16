"""Artifact registry — manages the artifact index for the agent system.

Each artifact produced during analysis (CSV tables, PNG figures, HTML reports,
etc.) is registered here with metadata for the frontend to render.

The artifact index is a list of ArtifactEntry dicts stored in AgentState.
"""
from __future__ import annotations

import base64
import hashlib
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


# ── Artifact type mapping ─────────────────────────────────────────────

EXT_TYPE_MAP = {
    # Tables
    ".csv": "table",
    ".tsv": "table",
    ".parquet": "table",
    ".xlsx": "table",
    ".xls": "table",
    ".biom": "table",
    # Figures
    ".png": "figure",
    ".jpg": "figure",
    ".jpeg": "figure",
    ".svg": "figure",
    ".gif": "figure",
    # Reports
    ".html": "report",
    ".htm": "report",
    ".md": "report",
    ".pdf": "report",
    # Logs
    ".txt": "log",
    ".log": "log",
    # Data / structured
    ".json": "data",
    ".yml": "data",
    ".yaml": "data",
    # Bioinformatics
    ".fna": "sequence",
    ".fasta": "sequence",
    ".fa": "sequence",
    ".fastq": "sequence",
    ".gz": "compressed",
    ".qza": "qiime_artifact",
    ".qzv": "qiime_visualization",
    ".newick": "tree",
    ".nwk": "tree",
}


# ── Preview generation ────────────────────────────────────────────────

def _preview_csv(path: str, max_rows: int = 5) -> Optional[str]:
    """Return the first few rows of a CSV as a string."""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            lines = []
            for i, line in enumerate(f):
                if i >= max_rows + 1:  # +1 for header
                    break
                lines.append(line.rstrip())
        return "\n".join(lines) if lines else None
    except Exception:
        return None


def _preview_image_base64(path: str, max_bytes: int = 50_000) -> Optional[str]:
    """Return a base64-encoded thumbnail for small images."""
    try:
        size = os.path.getsize(path)
        if size > max_bytes:
            return f"[Image: {size:,} bytes — too large for inline preview]"
        with open(path, "rb") as f:
            data = f.read()
        ext = os.path.splitext(path)[1].lower().lstrip(".")
        mime = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg",
                "svg": "image/svg+xml", "gif": "image/gif"}.get(ext, "image/png")
        b64 = base64.b64encode(data).decode("ascii")
        return f"data:{mime};base64,{b64}"
    except Exception:
        return None


def _preview_text(path: str, max_chars: int = 500) -> Optional[str]:
    """Return the first N characters of a text file."""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read(max_chars)
    except Exception:
        return None


def generate_preview(path: str, art_type: str) -> Optional[str]:
    """Generate a lightweight preview for an artifact based on its type."""
    if art_type == "table":
        return _preview_csv(path)
    elif art_type == "figure":
        return _preview_image_base64(path)
    elif art_type in ("report", "log", "data"):
        return _preview_text(path)
    return None


# ── Scanning and registration ─────────────────────────────────────────

def _normalize_artifact_path(path: str) -> str:
    """Return a canonical absolute path for artifact identity checks."""
    return os.path.normpath(os.path.abspath(path))


def _artifact_id_from_path(path: str, filename: str) -> str:
    """Build a stable ID from canonical path so repeated scans reuse identity."""
    canon = _normalize_artifact_path(path)
    digest = hashlib.sha1(canon.encode("utf-8")).hexdigest()[:12]
    safe_name = filename.replace(" ", "_")
    return f"artifact_{safe_name}_{digest}"


def _artifact_identity_key(artifact: Dict[str, Any]) -> str:
    """Resolve the key used for latest-only upsert semantics."""
    path = artifact.get("path")
    if isinstance(path, str) and path:
        return _normalize_artifact_path(path)
    rel = artifact.get("relative_path")
    if isinstance(rel, str) and rel:
        return f"rel::{os.path.normpath(rel)}"
    art_id = artifact.get("id")
    if isinstance(art_id, str) and art_id:
        return f"id::{art_id}"
    fname = artifact.get("filename") or artifact.get("name") or "unknown"
    return f"name::{fname}"


def scan_directory(
    directory: str,
    step_id: str = "unknown",
    run_id: str = "",
    generate_previews: bool = True,
) -> List[Dict[str, Any]]:
    """Scan a directory and return artifact entries for all files found.

    Parameters
    ----------
    directory : str
        Path to the directory to scan.
    step_id : str
        The step that produced these artifacts.
    generate_previews : bool
        Whether to generate preview content.

    Returns
    -------
    list of dict
        Artifact entries ready to merge into artifact_index.
    """
    entries: List[Dict[str, Any]] = []
    if not os.path.isdir(directory):
        return entries

    # Walk recursively to find all files (workflow outputs are nested)
    for root, _dirs, files in os.walk(directory):
        for fname in sorted(files):
            if fname.startswith("."):
                continue
            fpath = os.path.join(root, fname)
            if not os.path.isfile(fpath):
                continue
            # Skip sandbox temp scripts and other non-output artifacts
            if fname.startswith("tmp") and fname.endswith(".py"):
                continue
            if fname.startswith("tmp") and fname.endswith(".R"):
                continue
            if fname.endswith(".pyc") or fname == "__pycache__":
                continue
            if fname.endswith(".Rout") or fname == ".Rhistory":
                continue

            # Use relative path from base directory for readable IDs
            rel_path = os.path.relpath(fpath, directory)
            ext = os.path.splitext(fname)[1].lower()
            art_type = EXT_TYPE_MAP.get(ext, "other")

            preview = None
            if generate_previews:
                preview = generate_preview(fpath, art_type)

            canon = _normalize_artifact_path(fpath)
            entries.append({
                "id": _artifact_id_from_path(canon, fname),
                "type": art_type,
                "path": canon,
                "filename": fname,
                "relative_path": rel_path,
                "step_id": step_id,
                "run_id": run_id or "",
                "preview": preview,
                "size_bytes": os.path.getsize(fpath),
                "created_at": datetime.now(timezone.utc).isoformat(),
            })

    return entries


def merge_artifacts(
    existing: List[Dict[str, Any]],
    new: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Merge with latest-only semantics keyed by canonical artifact path."""
    merged = list(existing)
    index_by_key: Dict[str, int] = {}

    # Build index from existing artifacts and backfill stable IDs when missing.
    for i, art in enumerate(merged):
        if not isinstance(art, dict):
            continue
        if not art.get("id"):
            art["id"] = _artifact_id_from_path(
                str(art.get("path") or art.get("relative_path") or art.get("filename") or f"legacy-{i}"),
                str(art.get("filename") or art.get("name") or f"artifact-{i}"),
            )
        key = _artifact_identity_key(art)
        index_by_key[key] = i

    # Upsert latest artifact per key.
    for art in new:
        if not isinstance(art, dict):
            continue
        if not art.get("id"):
            art["id"] = _artifact_id_from_path(
                str(art.get("path") or art.get("relative_path") or art.get("filename") or "unknown"),
                str(art.get("filename") or art.get("name") or "artifact"),
            )
        key = _artifact_identity_key(art)
        if key in index_by_key:
            merged[index_by_key[key]] = {**merged[index_by_key[key]], **art}
        else:
            merged.append(art)
            index_by_key[key] = len(merged) - 1
    return merged
