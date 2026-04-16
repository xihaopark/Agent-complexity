"""wf_manager — Workflow CRUD module (parallel to datasets.py / experiments.py).

Manages workflows stored in renzo/workflow_pool/.  Each workflow is a
directory containing at minimum a manifest.json.  Agent-driven workflows
additionally carry a know-how document and optional bundled dataset.
"""
from __future__ import annotations

import json
import logging
import os
import shutil
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from renzo.app.workflows.registry import discover_workflows, get_workflow_by_id
from renzo.app.workflows.models import WorkflowInfo

logger = logging.getLogger(__name__)

WORKFLOW_POOL = Path(
    os.environ.get("WORKFLOW_POOL_DIR", str(Path(__file__).parent.parent / "workflow_pool"))
).resolve()
WORKFLOW_POOL.mkdir(parents=True, exist_ok=True)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _workflow_doc_paths(wf: WorkflowInfo) -> List[Path]:
    wf_dir = Path(wf.path)
    doc_names: List[str] = []
    if wf.know_how:
        doc_names.append(wf.know_how)
    doc_names.extend(wf.know_how_files or [])
    paths: List[Path] = []
    seen: set[str] = set()
    for name in doc_names:
        if not name:
            continue
        path = Path(name)
        full_path = path if path.is_absolute() else (wf_dir / path)
        key = str(full_path.resolve()) if full_path.exists() else str(full_path)
        if key in seen:
            continue
        seen.add(key)
        paths.append(full_path)
    return paths


def _serialize_workflow(wf: WorkflowInfo) -> Dict[str, Any]:
    data = wf.model_dump()
    data["step_count"] = len(data.get("steps") or [])
    data["has_know_how"] = bool(_workflow_doc_paths(wf))
    data["know_how_doc_count"] = len(_workflow_doc_paths(wf))
    data["has_dataset"] = bool(data.get("dataset_dir"))
    return data


# ── Read ────────────────────────────────────────────────────────────────

def list_workflows(status: Optional[str] = None) -> List[Dict[str, Any]]:
    """List all discovered workflows with enriched metadata."""
    wfs = discover_workflows()
    results = []
    for wf in wfs:
        results.append(_serialize_workflow(wf))
    return results


def get_workflow(wf_id: str) -> Optional[Dict[str, Any]]:
    """Get full workflow detail by ID."""
    wf = get_workflow_by_id(wf_id)
    if not wf:
        return None
    return _serialize_workflow(wf)


def get_workflow_steps(wf_id: str) -> Optional[List[Dict[str, Any]]]:
    """Return the steps array from the workflow manifest."""
    wf = get_workflow(wf_id)
    if not wf:
        return None
    return wf.get("steps", [])


def get_workflow_know_how_documents(wf_id: str) -> List[Dict[str, str]]:
    """Read workflow know-how and skill documents in discovery order."""
    wf = get_workflow_by_id(wf_id)
    if not wf:
        return []
    documents: List[Dict[str, str]] = []
    for path in _workflow_doc_paths(wf):
        if not path.is_file():
            logger.warning("Know-how file not found: %s", path)
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except Exception as e:
            logger.error("Failed to read know-how %s: %s", path, e)
            continue
        documents.append({
            "id": path.stem.lower().replace(" ", "_").replace("-", "_"),
            "name": path.stem.replace("_", " ").replace("-", " ").title(),
            "path": str(path.resolve()),
            "content": content,
        })
    return documents


def get_workflow_know_how(wf_id: str) -> Optional[str]:
    """Read and return the know-how document content for a workflow."""
    docs = get_workflow_know_how_documents(wf_id)
    if not docs:
        return None
    if len(docs) == 1:
        return docs[0]["content"]
    return "\n\n".join(
        f"--- {doc['name']} ({Path(doc['path']).name}) ---\n{doc['content']}"
        for doc in docs
    )


def get_workflow_dataset_dir(wf_id: str) -> Optional[Path]:
    """Return the absolute path to the bundled dataset directory."""
    wf = get_workflow_by_id(wf_id)
    if not wf or not wf.dataset_dir:
        return None
    ds_path = Path(wf.path) / wf.dataset_dir
    if ds_path.is_dir():
        return ds_path
    return None


# ── Create ──────────────────────────────────────────────────────────────

def create_workflow(
    name: str,
    engine: str = "agent",
    description: str = "",
    steps: Optional[List[Dict]] = None,
    know_how_content: Optional[str] = None,
    input_hints: Optional[List[str]] = None,
    output_hints: Optional[List[str]] = None,
    version: str = "1.0",
) -> Dict[str, Any]:
    """Create a new workflow in workflow_pool/."""
    wf_id = f"wf-{uuid.uuid4().hex[:12]}"
    wf_dir = WORKFLOW_POOL / wf_id
    wf_dir.mkdir(parents=True, exist_ok=True)

    # Write know-how file if provided
    know_how_filename = None
    if know_how_content:
        know_how_filename = "know-how.md"
        (wf_dir / know_how_filename).write_text(know_how_content, encoding="utf-8")

    manifest = {
        "id": wf_id,
        "name": name,
        "engine": engine,
        "description": description,
        "version": version,
        "know_how": know_how_filename,
        "know_how_files": [know_how_filename] if know_how_filename else [],
        "dataset_dir": None,
        "default_dataset_ids": [],
        "aliases": [],
        "tags": [],
        "discovery": {},
        "input_hints": input_hints or [],
        "output_hints": output_hints or [],
        "steps": steps or [],
        "created_at": _now_iso(),
        "updated_at": _now_iso(),
    }
    (wf_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    logger.info("Created workflow %s: %s", wf_id, name)
    return manifest


# ── Update ──────────────────────────────────────────────────────────────

def update_workflow(wf_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Update workflow manifest fields."""
    wf = get_workflow_by_id(wf_id, WORKFLOW_POOL)
    if not wf:
        return None
    manifest_path = Path(wf.path) / "manifest.json"
    if not manifest_path.is_file():
        return None

    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception:
        return None

    allowed = {"name", "description", "steps", "input_hints", "output_hints",
               "default_dataset_ids", "dataset_dir", "know_how", "know_how_files",
               "version", "engine", "aliases", "tags", "discovery"}
    for k, v in updates.items():
        if k in allowed:
            data[k] = v
    data["updated_at"] = _now_iso()

    manifest_path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    logger.info("Updated workflow %s", wf_id)
    return data


# ── Delete ──────────────────────────────────────────────────────────────

def delete_workflow(wf_id: str) -> bool:
    """Delete a workflow directory."""
    wf = get_workflow_by_id(wf_id, WORKFLOW_POOL)
    if not wf:
        return False
    wf_dir = Path(wf.path)
    if wf_dir.is_dir():
        shutil.rmtree(wf_dir, ignore_errors=True)
        logger.info("Deleted workflow %s", wf_id)
        return True
    return False


# ── Dataset linking ─────────────────────────────────────────────────────

def link_workflow_dataset(wf_id: str, dataset_ids: List[str]) -> Optional[Dict[str, Any]]:
    """Set default_dataset_ids on a workflow manifest."""
    return update_workflow(wf_id, {"default_dataset_ids": dataset_ids})
