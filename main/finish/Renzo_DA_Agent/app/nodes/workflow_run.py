"""Workflow run node: execute Nextflow/Snakemake workflows."""
from __future__ import annotations

import logging
import os
import shutil
import time
import uuid
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from renzo.app.state import AgentState
from renzo.app.workflows import get_workflow_by_id
from renzo.app.workflows.executor import WorkflowExecutor

logger = logging.getLogger(__name__)

_WORKFLOWS_DATA = Path(__file__).resolve().parent.parent.parent / "data" / "workflows"


def cleanup_old_workflow_runs(
    keep_last_n: Optional[int] = 20,
    max_age_days: Optional[int] = 7,
) -> int:
    """Delete old agent-{workflow_id}-{suffix} run directories under data/workflows.
    Keeps the newest keep_last_n dirs and deletes dirs older than max_age_days.
    Returns number of directories removed."""
    if not _WORKFLOWS_DATA.exists() or not _WORKFLOWS_DATA.is_dir():
        return 0
    dirs: List[Tuple[float, Path]] = []
    for entry in _WORKFLOWS_DATA.iterdir():
        if entry.is_dir() and entry.name.startswith("agent-"):
            try:
                mtime = entry.stat().st_mtime
                dirs.append((mtime, entry))
            except OSError:
                continue
    dirs.sort(key=lambda x: x[0], reverse=True)
    to_remove: List[Path] = []
    now = time.time()
    for i, (mtime, path) in enumerate(dirs):
        if keep_last_n is not None and i >= keep_last_n:
            to_remove.append(path)
        elif max_age_days is not None and max_age_days > 0:
            if (now - mtime) > max_age_days * 86400:
                to_remove.append(path)
    removed = 0
    for path in to_remove:
        try:
            shutil.rmtree(path)
            logger.info("Removed old workflow run dir: %s", path.name)
            removed += 1
        except OSError as e:
            logger.warning("Failed to remove %s: %s", path, e)
    return removed


def workflow_run_node(state: AgentState) -> Dict:
    """
    Run a registered workflow. Uses workflow_id_requested from state.
    Input path can come from data_profile.file_path or uploads.
    """
    workflow_id = state.get("workflow_id_requested")
    if not workflow_id:
        return {
            "next_node": "responder",
            "workflow_status": "skipped",
            "execution_logs": state.get("execution_logs", []) + [{
                "run_id": "wf-skip",
                "status": "skipped",
                "stdout": "",
                "stderr": "No workflow_id_requested in state.",
            }],
        }

    wf = get_workflow_by_id(workflow_id)
    if not wf:
        return {
            "next_node": "responder",
            "workflow_status": "failed",
            "workflow_run_id": None,
            "execution_logs": state.get("execution_logs", []) + [{
                "run_id": "wf-fail",
                "status": "error",
                "stdout": "",
                "stderr": f"Workflow '{workflow_id}' not found.",
            }],
        }

    # Resolve input path from data_profile or uploads
    data_profile = state.get("data_profile") or {}
    input_path = data_profile.get("file_path")
    if not input_path or not os.path.exists(input_path):
        uploads_dir = os.path.join(os.getcwd(), "renzo", "data", "uploads")
        if os.path.isdir(uploads_dir):
            candidates = [f for f in os.listdir(uploads_dir) if not f.startswith(".")]
            if candidates:
                input_path = os.path.join(uploads_dir, candidates[0])

    run_suffix = str(uuid.uuid4())[:8]
    work_dir = _WORKFLOWS_DATA / f"agent-{workflow_id}-{run_suffix}"
    work_dir.mkdir(parents=True, exist_ok=True)

    ex = WorkflowExecutor()
    params = dict(state.get("workflow_params") or {})

    if wf.engine == "nextflow":
        result = ex.run_nextflow(
            workflow_path=wf.path,
            work_dir=work_dir,
            params={k: v for k, v in params.items() if k != "config"},
            profile="docker",
            input_path=input_path,
        )
    elif wf.engine == "snakemake":
        result = ex.run_snakemake(
            workflow_path=wf.path,
            work_dir=work_dir,
            params=params,
            use_singularity=False,
            config=params.get("config"),
        )
    else:
        return {
            "next_node": "responder",
            "workflow_status": "failed",
            "execution_logs": state.get("execution_logs", []) + [{
                "run_id": "wf-fail",
                "status": "error",
                "stderr": f"Unsupported engine: {wf.engine}",
            }],
        }

    logs = list(state.get("execution_logs", []))
    logs.append({
        "run_id": f"wf-{workflow_id}",
        "status": result.status,
        "stdout": result.stdout or "",
        "stderr": result.stderr or "",
        "output_paths": result.output_paths,
    })

    return {
        "workflow_run_id": f"wf-{workflow_id}",
        "workflow_status": result.status,
        "execution_logs": logs,
        "artifact_index": (state.get("artifact_index") or []) + [
            {"name": p, "type": "file", "path": p}
            for p in (result.output_paths or [])[:20]
        ],
        "next_node": "responder",
    }
