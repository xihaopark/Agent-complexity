"""Workflow registry: scan workflow_pool and expose discovered workflows."""
from __future__ import annotations

import json
import logging
import os
import tempfile
import zipfile
from pathlib import Path
from typing import List, Optional

from renzo.app.workflows.models import WorkflowInfo
from renzo.app.workflows.ro_crate import parse_ro_crate

logger = logging.getLogger(__name__)


def _default_workflow_pool_path() -> Path:
    """Default path to workflow pool (supports container override)."""
    env_path = os.environ.get("WORKFLOW_POOL_DIR")
    if env_path:
        return Path(env_path).resolve()
    # __file__ = renzo/app/workflows/registry.py → 3 levels up = renzo/
    base = Path(__file__).resolve().parent.parent.parent
    return (base / "workflow_pool").resolve()


def _default_discovery_roots() -> List[Path]:
    base = Path(__file__).resolve().parent.parent.parent
    roots: List[Path] = [_default_workflow_pool_path()]
    env_paths = os.environ.get("WORKFLOW_DISCOVERY_DIRS", "").strip()
    if env_paths:
        roots.extend(Path(item).resolve() for item in env_paths.split(os.pathsep) if item.strip())
    finish_root = base.parent
    if (finish_root / "run_finish_workflow.py").exists():
        roots.append(finish_root.resolve())
    unique_roots: List[Path] = []
    seen: set[str] = set()
    for root in roots:
        key = str(root)
        if key in seen:
            continue
        seen.add(key)
        unique_roots.append(root)
    return unique_roots


def _parse_manifest(workflow_dir: Path) -> Optional[WorkflowInfo]:
    """Parse a manifest.json file for non-RO-Crate workflows (e.g., R pipelines).

    Expected format:
    {
        "id": "clinical-pilot5",
        "name": "FDA Pilot 5 Clinical Pipeline",
        "engine": "r",
        "entry_point": "run-all-adams-tlfs.r",
        "description": "...",
        "input_hints": ["xpt", "dataset-json"],
        "output_hints": ["adam-xpt", "tlf-rtf", "tlf-pdf"]
    }
    """
    manifest_path = workflow_dir / "manifest.json"
    if not manifest_path.exists():
        return None

    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        info = WorkflowInfo(
            id=data.get("id", workflow_dir.name),
            name=data.get("name", workflow_dir.name),
            engine=data.get("engine", "r"),
            entry_point=data.get("entry_point", ""),
            path=str(workflow_dir.resolve()),
            description=data.get("description"),
            params_schema=data.get("params_schema", {}),
            input_hints=data.get("input_hints", []),
            output_hints=data.get("output_hints", []),
            version=data.get("version"),
            license=data.get("license"),
            url=data.get("url"),
            aliases=data.get("aliases", []),
            tags=data.get("tags", []),
            discovery=data.get("discovery", {}),
            # v2 fields
            know_how=data.get("know_how"),
            know_how_files=data.get("know_how_files", []),
            dataset_dir=data.get("dataset_dir"),
            default_dataset_ids=data.get("default_dataset_ids", []),
            steps=data.get("steps", []),
        )
        logger.info("Discovered manifest workflow: %s (%s)", info.name, info.engine)
        return info
    except Exception as e:
        logger.warning("Failed to parse manifest.json in %s: %s", workflow_dir, e)
        return None


def _merge_sidecar_manifest(workflow_dir: Path, info: WorkflowInfo) -> None:
    """Merge fields from an optional sidecar manifest.json into an RO-Crate WorkflowInfo.

    This allows RO-Crate workflows to carry extra metadata such as default_dataset_ids,
    know_how, steps, etc. without modifying the RO-Crate metadata itself.
    """
    manifest_path = workflow_dir / "manifest.json"
    if not manifest_path.exists():
        return
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception:
        return
    # Merge known fields
    if data.get("default_dataset_ids"):
        info.default_dataset_ids = data["default_dataset_ids"]
    if data.get("know_how"):
        info.know_how = data["know_how"]
    if data.get("know_how_files"):
        info.know_how_files = data["know_how_files"]
    if data.get("dataset_dir"):
        info.dataset_dir = data["dataset_dir"]
    if data.get("steps"):
        info.steps = data["steps"]
    if data.get("aliases"):
        info.aliases = data["aliases"]
    if data.get("tags"):
        info.tags = data["tags"]
    if data.get("discovery"):
        info.discovery = data["discovery"]


def _discover_from_root(root: Path, workflows: List[WorkflowInfo], seen_ids: set[str]) -> None:
    if not root.exists() or not root.is_dir():
        return

    for item in sorted(root.iterdir()):
        if not item.is_dir() or item.name.startswith("."):
            continue

        meta = item / "ro-crate-metadata.json"
        if meta.exists():
            info = parse_ro_crate(item)
            if info and info.id not in seen_ids:
                _merge_sidecar_manifest(item, info)
                seen_ids.add(info.id)
                workflows.append(info)
            continue

        info = _parse_manifest(item)
        if info and info.id not in seen_ids:
            seen_ids.add(info.id)
            workflows.append(info)

    for item in sorted(root.iterdir()):
        if not item.is_file() or item.suffix != ".zip" or ".crate" not in item.stem:
            continue
        try:
            with zipfile.ZipFile(item, "r") as zf:
                names = zf.namelist()
                if "ro-crate-metadata.json" not in names:
                    continue
                with tempfile.TemporaryDirectory(prefix="renzo_crate_") as tmp:
                    zf.extractall(tmp)
                    tmp_path = Path(tmp)
                    meta_in_root = tmp_path / "ro-crate-metadata.json"
                    if meta_in_root.exists():
                        info = parse_ro_crate(tmp_path)
                    else:
                        subdirs = [d for d in tmp_path.iterdir() if d.is_dir()]
                        info = None
                        for sub in subdirs:
                            if (sub / "ro-crate-metadata.json").exists():
                                info = parse_ro_crate(sub)
                                break
                    if info and info.id not in seen_ids:
                        info.path = str(item.resolve())
                        seen_ids.add(info.id)
                        workflows.append(info)
        except (zipfile.BadZipFile, OSError):
            continue


def discover_workflows(pool_path: Path | None = None) -> List[WorkflowInfo]:
    """
    Scan workflow_pool for workflows:
    1. RO-Crate directories (ro-crate-metadata.json) — Nextflow/Snakemake
    2. manifest.json directories — R pipelines and other engines
    3. .crate.zip files — packed RO-Crate workflows

    Returns list of WorkflowInfo for all discovered workflows.
    """
    workflows: List[WorkflowInfo] = []
    seen_ids: set[str] = set()
    roots = [pool_path.resolve()] if pool_path else _default_discovery_roots()
    for root in roots:
        _discover_from_root(root, workflows, seen_ids)

    return workflows


def get_workflow_by_id(workflow_id: str, pool_path: Path | None = None) -> WorkflowInfo | None:
    """Return WorkflowInfo for the given id, or None."""
    for wf in discover_workflows(pool_path):
        if wf.id == workflow_id:
            return wf
    return None


def get_workflow_path(workflow_id: str, pool_path: Path | None = None) -> Path | None:
    """
    Return the resolved path to the workflow directory.
    For .crate.zip we return the zip path; caller must unpack for execution.
    """
    wf = get_workflow_by_id(workflow_id, pool_path)
    if not wf:
        return None
    p = Path(wf.path)
    if p.exists():
        return p
    return None
