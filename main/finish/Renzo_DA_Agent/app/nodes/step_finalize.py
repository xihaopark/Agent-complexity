"""step_finalize node — wraps up a step's outputs and updates the artifact index.

This node runs after QC passes (or after a terminal failure) to:
  1. Scan the outputs directory for new files (both code artifacts AND workflow outputs).
  2. Register them in artifact_index via the artifacts module.
  3. Mark the current plan step as completed/failed.
  4. Route to responder for the user-facing summary.
"""
from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Dict, List

from renzo.app.state import AgentState
from renzo.app.artifacts import merge_artifacts, scan_directory
from renzo.app.experiments import (
    get_experiment_dir,
    get_session_output_dir,
    resolve_execution_workdir,
)
from renzo.app.models.workflow_step import WorkflowPlan, StepStatus


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _collect_scan_dirs(state: AgentState) -> List[str]:
    """Collect all directories that should be scanned for artifacts."""
    dirs: List[str] = []
    seen: set[str] = set()

    def _add_dir(path: str) -> None:
        norm = os.path.normpath(path)
        if norm in seen:
            return
        if os.path.isdir(norm):
            seen.add(norm)
            dirs.append(norm)

    # Canonical execution directory first (session output by default)
    explicit_workdir = state.get("execution_workdir")
    if explicit_workdir:
        _add_dir(explicit_workdir)

    exp_id = state.get("experiment_id")
    sess_id = state.get("session_id")
    artifact_policy = state.get("artifact_policy", "session")

    # If session is active, scan session output dir
    if not dirs and exp_id and sess_id:
        sess_out = get_session_output_dir(exp_id, sess_id)
        if sess_out and sess_out.is_dir():
            _add_dir(str(sess_out))
    elif not dirs and exp_id:
        # Fallback: experiment-level output dir
        exp_out = get_experiment_dir(exp_id, "output")
        if exp_out and exp_out.is_dir():
            _add_dir(str(exp_out))
    elif not dirs:
        # Fallback: scan the default shared artifacts dir
        code_dir = os.path.join(os.getcwd(), "renzo", "data", "artifacts")
        _add_dir(code_dir)

    # Ensure execution workdir is always represented if we can resolve it
    if exp_id or sess_id:
        resolved = resolve_execution_workdir(exp_id, sess_id, artifact_policy)
        _add_dir(str(resolved))

    # For workflow runs, also scan the workflow output directory
    wp = state.get("workflow_plan")
    if wp and isinstance(wp, dict):
        work_dir = wp.get("work_dir", "")
        if work_dir:
            output_dir = os.path.join(work_dir, "output")
            _add_dir(output_dir)

    # Compatibility read: include legacy shared path only when explicitly requested
    if artifact_policy in {"shared", "dual"}:
        shared_dir = os.path.join(os.getcwd(), "renzo", "data", "artifacts")
        _add_dir(shared_dir)

    return dirs


def _resolve_artifact_run_id(state: AgentState, run_ctx: Dict[str, str]) -> str:
    """Resolve the run id used for artifact traceability."""
    for candidate in (
        run_ctx.get("run_id"),
        state.get("workflow_run_id"),
    ):
        if isinstance(candidate, str) and candidate:
            return candidate

    logs = state.get("execution_logs", [])
    if logs and isinstance(logs[-1], dict):
        run_id = logs[-1].get("run_id")
        if isinstance(run_id, str) and run_id:
            return run_id
    return ""


def step_finalize_node(state: AgentState) -> Dict:
    current_step_id = state.get("current_step_id") or "unknown"
    validation = state.get("validation_result", {})
    step_succeeded = validation.get("status") in ("pass", "success", "warn")

    # ── Update plan step status ───────────────────────────────────────
    plan_steps = list(state.get("plan_steps", []))
    for step in plan_steps:
        if step.get("id") == current_step_id:
            step["status"] = "completed" if step_succeeded else "failed"
            break

    workflow_plan_out = state.get("workflow_plan")
    workflow_status = state.get("workflow_status")
    plan_status = state.get("plan_status", "executing")
    next_current_step = current_step_id

    run_ctx = dict(state.get("workflow_run_context") or {})
    execution_mode = run_ctx.get("execution_mode", "interactive")
    strict_manifest = bool(run_ctx.get("strict_manifest", True))

    if workflow_plan_out and isinstance(workflow_plan_out, dict):
        plan = WorkflowPlan.from_dict(workflow_plan_out)
        target_step = plan.get_step(current_step_id) or (
            plan.get_step(plan.current_step_id) if plan.current_step_id else None
        )
        if target_step:
            target_step.status = StepStatus.SUCCESS if step_succeeded else StepStatus.FAILED
            if not step_succeeded:
                target_step.error = validation.get("stderr_excerpt", "")[:500]

        if step_succeeded:
            if plan.is_complete():
                plan.status = "completed"
                workflow_status = "success"
                plan_status = "completed"
                run_ctx["status"] = "success"
                run_ctx["ended_at"] = run_ctx.get("ended_at") or _now_iso()
                next_current_step = current_step_id
            else:
                plan.status = "executing"
                next_step = plan.get_next_step(strict_manifest=strict_manifest)
                next_current_step = next_step.id if next_step else current_step_id
                if execution_mode == "interactive":
                    workflow_status = "waiting_user"
                    run_ctx["status"] = "waiting_user"
                else:
                    workflow_status = "running"
                    run_ctx["status"] = "running"
        else:
            plan.status = "failed"
            workflow_status = "failed"
            plan_status = "failed"
            run_ctx["status"] = "failed"
            run_ctx["error_summary"] = validation.get("stderr_excerpt", "")[:300]
            run_ctx["ended_at"] = run_ctx.get("ended_at") or _now_iso()

        run_ctx["current_step_id"] = next_current_step
        workflow_plan_out = plan.to_dict()
        plan_steps = plan.to_plan_steps()

    # ── Scan and register artifacts from ALL relevant dirs ─────────────
    artifact_run_id = _resolve_artifact_run_id(state, run_ctx)
    all_new_artifacts = []
    for scan_dir in _collect_scan_dirs(state):
        new_artifacts = scan_directory(
            scan_dir,
            step_id=current_step_id,
            run_id=artifact_run_id,
        )
        all_new_artifacts.extend(new_artifacts)

    artifact_index = merge_artifacts(
        state.get("artifact_index", []),
        all_new_artifacts,
    )

    logs = list(state.get("execution_logs", []))
    if logs:
        latest = dict(logs[-1])
        latest.update({
            "workflow_id": run_ctx.get("workflow_id", latest.get("workflow_id")),
            "step_id": current_step_id,
            "artifact_count": len(all_new_artifacts),
            "retry_count": state.get("retry_count", 0),
            "error_pattern_id": (validation.get("matched_pattern_ids") or [None])[0],
            "stdout_tail": (latest.get("stdout", "") or "")[-500:],
            "stderr_tail": (latest.get("stderr", "") or "")[-500:],
        })
        logs[-1] = latest

    # ── Always stop and report to the user after each step ──────────
    # The agent is conversational: it completes one meaningful chunk,
    # reports progress, and lets the user decide whether to continue.
    result = {
        "plan_steps": plan_steps,
        "artifact_index": artifact_index,
        "execution_logs": logs,
        "code_scratchpad": "",       # clear for next step
        "retry_count": 0,            # reset retries
        "validation_result": {},     # clear for next step
        "next_node": "responder",
    }
    if workflow_plan_out is not None:
        result.update({
            "workflow_plan": workflow_plan_out,
            "workflow_status": workflow_status,
            "workflow_run_context": run_ctx,
            "plan_status": plan_status,
            "current_step_id": next_current_step,
        })
    return result
