"""Dataset management — independent data entities that can be referenced by experiments.

Each dataset gets a dedicated directory:

    renzo/data/datasets/{dataset_id}/
        metadata.json    # name, description, tags, created_at
        files/           # actual data files (XPT, CSV, etc.)

Datasets are independent from experiments. Multiple experiments can reference
the same dataset via dataset_ids in their metadata.
"""
from __future__ import annotations

import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
import uuid
import logging

logger = logging.getLogger(__name__)

# ── Root directory ─────────────────────────────────────────────────────

_default_data_root = (Path(__file__).resolve().parent.parent / "data").resolve()
_data_root = Path(os.environ.get("DATA_ROOT", str(_default_data_root))).resolve()
DATASETS_ROOT = _data_root / "datasets"
DATASETS_ROOT.mkdir(parents=True, exist_ok=True)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# ── CRUD ───────────────────────────────────────────────────────────────

def create_dataset(
    name: str,
    description: str = "",
    tags: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Create a new dataset on disk. Returns metadata dict."""
    ds_id = f"ds-{uuid.uuid4().hex[:12]}"
    ds_dir = DATASETS_ROOT / ds_id
    (ds_dir / "files").mkdir(parents=True, exist_ok=True)

    metadata: Dict[str, Any] = {
        "id": ds_id,
        "name": name,
        "description": description,
        "tags": tags or [],
        "status": "active",
        "created_at": _now_iso(),
        "updated_at": _now_iso(),
        "file_count": 0,
        "total_size_bytes": 0,
    }
    _save_metadata(ds_id, metadata)
    logger.info("Created dataset %s at %s", ds_id, ds_dir)
    return metadata


def get_dataset(ds_id: str) -> Optional[Dict[str, Any]]:
    """Load dataset metadata from disk."""
    meta_path = DATASETS_ROOT / ds_id / "metadata.json"
    if not meta_path.exists():
        return None
    with open(meta_path, "r") as f:
        return json.load(f)


def list_datasets(status: Optional[str] = None) -> List[Dict[str, Any]]:
    """List all datasets, optionally filtered by status."""
    results = []
    if not DATASETS_ROOT.exists():
        return results
    for entry in sorted(DATASETS_ROOT.iterdir()):
        if not entry.is_dir():
            continue
        meta_path = entry / "metadata.json"
        if not meta_path.exists():
            continue
        with open(meta_path, "r") as f:
            meta = json.load(f)
        if status and meta.get("status") != status:
            continue
        _refresh_counts(meta)
        results.append(meta)
    results.sort(key=lambda m: m.get("created_at", ""), reverse=True)
    return results


def update_dataset(
    ds_id: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    status: Optional[str] = None,
    tags: Optional[List[str]] = None,
) -> Optional[Dict[str, Any]]:
    """Update dataset metadata fields."""
    meta = get_dataset(ds_id)
    if meta is None:
        return None
    if name is not None:
        meta["name"] = name
    if description is not None:
        meta["description"] = description
    if status is not None:
        meta["status"] = status
    if tags is not None:
        meta["tags"] = tags
    meta["updated_at"] = _now_iso()
    _save_metadata(ds_id, meta)
    return meta


def delete_dataset(ds_id: str) -> bool:
    """Delete a dataset and all its files."""
    ds_dir = DATASETS_ROOT / ds_id
    if not ds_dir.exists():
        return False
    shutil.rmtree(ds_dir)
    logger.info("Deleted dataset %s", ds_id)
    return True


# ── File operations ────────────────────────────────────────────────────

def list_dataset_files(ds_id: str) -> List[Dict[str, Any]]:
    """List files in a dataset (recursively, supporting subdirectories)."""
    files_dir = DATASETS_ROOT / ds_id / "files"
    if not files_dir.exists():
        return []
    files = []
    for entry in sorted(files_dir.rglob("*")):
        if entry.name.startswith("."):
            continue
        if entry.is_file():
            stat = entry.stat()
            ext = entry.suffix.lower()
            rel_path = entry.relative_to(files_dir)
            files.append({
                "name": str(rel_path),
                "type": _file_type(ext),
                "path": f"files/{rel_path}",
                "size_bytes": stat.st_size,
                "modified_at": datetime.fromtimestamp(
                    stat.st_mtime, tz=timezone.utc
                ).isoformat(),
            })
    return files


def save_dataset_file(ds_id: str, filename: str, content: bytes) -> Dict[str, Any]:
    """Save an uploaded file into the dataset. Supports nested paths like 'subdir/file.xpt'."""
    files_dir = DATASETS_ROOT / ds_id / "files"
    if not files_dir.exists():
        raise ValueError(f"Dataset {ds_id} not found")
    file_path = files_dir / filename
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(content)
    meta = get_dataset(ds_id)
    if meta:
        _refresh_counts(meta)
        _save_metadata(ds_id, meta)
    return {
        "filename": filename,
        "path": str(file_path),
        "size_bytes": len(content),
    }


def get_dataset_file_path(ds_id: str, relative_path: str) -> Optional[Path]:
    """Get absolute path of a file within a dataset (with security check)."""
    ds_dir = DATASETS_ROOT / ds_id
    file_path = (ds_dir / relative_path).resolve()
    if not str(file_path).startswith(str(ds_dir.resolve())):
        return None
    if not file_path.exists():
        return None
    return file_path


def delete_dataset_file(ds_id: str, filename: str) -> bool:
    """Delete a file from the dataset."""
    file_path = DATASETS_ROOT / ds_id / "files" / filename
    if not file_path.exists():
        return False
    file_path.unlink()
    meta = get_dataset(ds_id)
    if meta:
        _refresh_counts(meta)
        _save_metadata(ds_id, meta)
    return True


def get_dataset_files_dir(ds_id: str) -> Optional[Path]:
    """Return absolute path to a dataset's files/ directory."""
    files_dir = DATASETS_ROOT / ds_id / "files"
    if files_dir.exists():
        return files_dir
    return None


# ── Helpers ────────────────────────────────────────────────────────────

def _save_metadata(ds_id: str, meta: Dict[str, Any]) -> None:
    meta_path = DATASETS_ROOT / ds_id / "metadata.json"
    with open(meta_path, "w") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)


def _refresh_counts(meta: Dict[str, Any]) -> None:
    files_dir = DATASETS_ROOT / meta["id"] / "files"
    if files_dir.exists():
        file_list = [p for p in files_dir.rglob("*") if p.is_file()]
        meta["file_count"] = len(file_list)
        meta["total_size_bytes"] = sum(p.stat().st_size for p in file_list)
    else:
        meta["file_count"] = 0
        meta["total_size_bytes"] = 0
    meta["updated_at"] = _now_iso()


def _file_type(ext: str) -> str:
    type_map = {
        ".csv": "table", ".tsv": "table", ".parquet": "table",
        ".xlsx": "table", ".xls": "table", ".xpt": "data",
        ".png": "figure", ".jpg": "figure", ".jpeg": "figure",
        ".svg": "figure", ".gif": "figure",
        ".html": "report", ".htm": "report", ".pdf": "report", ".md": "report",
        ".txt": "text", ".log": "text",
        ".json": "data", ".yml": "data", ".yaml": "data",
        ".r": "code", ".R": "code", ".py": "code",
        ".rds": "data", ".rda": "data",
    }
    return type_map.get(ext, "other")
