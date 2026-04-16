from __future__ import annotations

import os
import re
import shutil
from pathlib import Path
from typing import Dict, Optional

from renzo.app.state import AgentState
from renzo.app.sandbox.docker_env import DockerSandbox
from renzo.app.sandbox.local_env import LocalSandbox
from renzo.app.models.workflow_step import WorkflowPlan, WorkflowStep, StepStatus, WorkflowEngine
from renzo.app.runners.snakemake_runner import SnakemakeRunner
from renzo.app.runners.nextflow_runner import NextflowRunner
from renzo.app.experiments import resolve_execution_workdir


PYTHON_ALLOWLIST = {"numpy", "pandas", "scipy", "scikit-learn", "matplotlib", "seaborn"}
R_ALLOWLIST = {"haven", "admiral", "dplyr", "tidyr", "ggplot2", "rtables", "gtsummary",
               "xportr", "datasetjson", "metacore", "metatools", "stringr", "lubridate"}
MAX_INSTALL_ATTEMPTS = 1


def _detect_language(code: str) -> str:
    """Detect whether code is R or Python based on markers.

    R code must start with '#!R', '# R code', or '# R script'.
    Everything else is treated as Python.
    """
    stripped = code.strip()
    if (
        stripped.startswith("#!R")
        or stripped.startswith("# R code")
        or stripped.startswith("# R script")
    ):
        return "r"
    return "python"


def _strip_r_marker(code: str) -> str:
    """Remove the R language marker from the first line."""
    return re.sub(r"^#!R|^# R code|^# R script", "", code, count=1).strip()


def _extract_missing_module(stderr: str) -> str | None:
    match = re.search(r"No module named ['\"]([^'\"]+)['\"]", stderr)
    if match:
        return match.group(1)
    return None


def _extract_missing_r_package(stderr: str) -> str | None:
    """Extract missing R package name from error output."""
    match = re.search(r"there is no package called ['\"]([^'\"]+)['\"]", stderr)
    if match:
        return match.group(1)
    return None


def _get_sandbox():
    """Get appropriate sandbox based on environment."""
    sandbox_mode = os.environ.get("SANDBOX_MODE", "local").lower()
    docker_available = shutil.which("docker") is not None
    if sandbox_mode == "docker" and docker_available:
        return DockerSandbox()
    return LocalSandbox()


def _resolve_working_dir(state: AgentState) -> str:
    """Determine the working directory for code execution.

    Priority:
    1. Session-specific output dir: experiments/{exp_id}/sessions/{sess_id}/output/
    2. Experiment-level fallback: experiments/{exp_id}/output/
    3. Shared artifacts dir: renzo/data/artifacts/
    """
    explicit = state.get("execution_workdir")
    if explicit:
        os.makedirs(explicit, exist_ok=True)
        return explicit

    exp_id = state.get("experiment_id")
    sess_id = state.get("session_id")
    artifact_policy = state.get("artifact_policy", "session")
    resolved = resolve_execution_workdir(exp_id, sess_id, artifact_policy)
    resolved.mkdir(parents=True, exist_ok=True)
    return str(resolved)


def _execute_code(state: AgentState) -> Dict:
    """Execute Python or R code via sandbox, with auto-detection."""
    code = state.get("code_scratchpad", "")
    if not code:
        return {"next_node": "planner"}

    working_dir = _resolve_working_dir(state)
    os.makedirs(working_dir, exist_ok=True)
    sandbox = _get_sandbox()

    # Detect language and route accordingly
    language = state.get("code_language") or _detect_language(code)

    if language == "r":
        actual_code = _strip_r_marker(code)
        result = sandbox.run_r_code(actual_code, working_dir)
    else:
        actual_code = code
        result = sandbox.run_code(code, working_dir)

    logs = list(state.get("execution_logs", []))
    run_ctx = dict(state.get("workflow_run_context") or {})
    workflow_id = run_ctx.get("workflow_id") or state.get("workflow_id_requested")
    current_step_id = state.get("current_step_id")
    if workflow_id and current_step_id:
        run_id = f"wf-{workflow_id}-{current_step_id}-{len(logs) + 1}"
    else:
        run_id = f"run-{len(logs) + 1}"
    log_entry = {
        "run_id": run_id,
        "workflow_id": workflow_id,
        "step_id": current_step_id,
        "status": result["status"],
        "stdout": result["stdout"],
        "stderr": result["stderr"],
        "language": language,
        "retry_count": state.get("retry_count", 0),
        "working_dir": working_dir,
    }
    logs.append(log_entry)

    # Auto-install missing packages and retry
    if result["status"] == "error":
        if language == "r":
            missing = _extract_missing_r_package(result["stderr"])
            if missing and missing.lower() in {p.lower() for p in R_ALLOWLIST} and MAX_INSTALL_ATTEMPTS > 0:
                install_result = sandbox.install_r_packages([missing], working_dir)
                log_entry["install"] = install_result
                if install_result.get("status") == "success":
                    retry = sandbox.run_r_code(actual_code, working_dir)
                    log_entry["retry"] = retry
                    log_entry["status"] = retry["status"]
                    log_entry["stdout"] = retry["stdout"]
                    log_entry["stderr"] = retry["stderr"]
        else:
            missing = _extract_missing_module(result["stderr"])
            if missing and missing in PYTHON_ALLOWLIST and MAX_INSTALL_ATTEMPTS > 0:
                install_result = sandbox.install_packages([missing], working_dir)
                log_entry["install"] = install_result
                if install_result.get("status") == "success":
                    retry = sandbox.run_code(code, working_dir)
                    log_entry["retry"] = retry
                    log_entry["status"] = retry["status"]
                    log_entry["stdout"] = retry["stdout"]
                    log_entry["stderr"] = retry["stderr"]

    # Note: executor always flows to step_validate via fixed edge in graph.
    return {
        "execution_logs": logs,
        "code_language": language,
        "execution_workdir": working_dir,
    }


def _execute_workflow_step(state: AgentState) -> Dict:
    """Execute next workflow step via runner."""
    plan_data = state.get("workflow_plan")
    if not plan_data:
        return {"workflow_status": "failed"}

    plan = WorkflowPlan.from_dict(plan_data)
    run_ctx = dict(state.get("workflow_run_context") or {})
    strict_manifest = bool(run_ctx.get("strict_manifest", True))
    step = None
    current_step_id = state.get("current_step_id") or plan.current_step_id
    if current_step_id:
        candidate = plan.get_step(str(current_step_id))
        completed = plan.completed_step_ids()
        available_refs = plan.available_refs()
        if candidate and candidate.can_run(
            completed,
            available_refs=available_refs,
            strict_manifest=strict_manifest,
        ):
            step = candidate
    if step is None:
        step = plan.get_next_step(strict_manifest=strict_manifest)
    if not step:
        # No more steps — let step_validate handle the outcome
        if plan.is_complete():
            plan.status = "completed"
            return {
                "workflow_plan": plan.to_dict(),
                "workflow_status": "success",
            }
        if plan.has_failed():
            plan.status = "failed"
            return {
                "workflow_plan": plan.to_dict(),
                "workflow_status": "failed",
            }
        return {}

    # Mark step as running
    step.status = StepStatus.RUNNING
    plan.current_step_id = step.id
    plan.status = "executing"

    # Select runner based on engine
    runner = None
    if step.engine == WorkflowEngine.SNAKEMAKE:
        runner = SnakemakeRunner()
    elif step.engine == WorkflowEngine.NEXTFLOW:
        runner = NextflowRunner()
    elif step.engine == WorkflowEngine.PYTHON:
        # Use sandbox for Python code
        sandbox = _get_sandbox()
        if step.code:
            result = sandbox.run_code(step.code, plan.work_dir)
            step.stdout = result.get("stdout", "")
            step.stderr = result.get("stderr", "")
            if result["status"] == "success":
                step.status = StepStatus.SUCCESS
            else:
                step.status = StepStatus.FAILED
                step.error = result.get("stderr", "")[:500]
                step.retry_count += 1
        else:
            step.status = StepStatus.SKIPPED
        return {
            "workflow_plan": plan.to_dict(),
            "workflow_status": "running",
        }

    if not runner:
        step.status = StepStatus.FAILED
        step.error = f"Unknown engine: {step.engine}"
        return {
            "workflow_plan": plan.to_dict(),
            "workflow_status": "failed",
        }

    # Check if runner is available, try to install if not
    if not runner.check_available():
        if not runner.install_if_missing():
            diag = dict(getattr(runner, "last_install_diagnostics", {}) or {})
            message = diag.get("message", f"Runner not available: {step.engine}")
            hint = diag.get("hint")
            step.status = StepStatus.FAILED
            step.error = f"{message} Hint: {hint}" if hint else message
            step.stderr = diag.get("stderr_tail", "")
            step.retry_count += 1
            return {
                "workflow_plan": plan.to_dict(),
                "workflow_status": "failed",
            }

    # Execute step
    result = runner.run_step(
        workflow_dir=Path(plan.workflow_dir),
        work_dir=Path(plan.work_dir),
        targets=step.targets if step.targets else None,
        params=step.params,
        timeout=step.timeout,
    )

    # Update step with results
    step.stdout = result.stdout
    step.stderr = result.stderr
    step.artifacts = result.artifacts

    if result.status == "success":
        step.status = StepStatus.SUCCESS
    else:
        step.status = StepStatus.FAILED
        step.error = result.error
        step.retry_count += 1

    # Update logs
    logs = list(state.get("execution_logs", []))
    workflow_id = run_ctx.get("workflow_id") or plan.workflow_id
    logs.append({
        "run_id": f"wf-{plan.id}-{step.id}",
        "workflow_id": workflow_id,
        "step_id": step.id,
        "status": result.status,
        "stdout": result.stdout[:4000],
        "stderr": result.stderr[:4000],
        "artifacts": result.artifacts[:10],
        "retry_count": step.retry_count,
        "working_dir": plan.work_dir,
        "metadata": dict(result.metadata or {}),
    })

    return {
        "workflow_plan": plan.to_dict(),
        "workflow_status": "running",
        "execution_logs": logs,
        "execution_workdir": plan.work_dir,
    }


def executor_node(state: AgentState) -> Dict:
    """Unified executor node — handles code (Python/R) and workflow step execution.

    After execution, the graph routes to step_validate (fixed edge).

    Routing logic:
    - If workflow_plan exists and has pending steps -> execute workflow step
    - If code_scratchpad has code -> detect language (Python/#!R) and execute
    - Otherwise -> empty result (step_validate will handle)
    """
    # Check if we have a workflow plan with pending steps
    plan_data = state.get("workflow_plan")
    if plan_data:
        plan = WorkflowPlan.from_dict(plan_data)
        strict_manifest = bool((state.get("workflow_run_context") or {}).get("strict_manifest", True))
        if plan.get_next_step(strict_manifest=strict_manifest) is not None:
            return _execute_workflow_step(state)

    # Check if we have code to execute
    code = state.get("code_scratchpad", "")
    if code:
        return _execute_code(state)

    # Nothing to execute — step_validate will catch this
    return {}
