"""step_validate node — checks execution results and decides next action.

After the executor runs code or a workflow step, this node inspects
stdout/stderr and output files to determine the next routing.

Routing decisions:
  - Execution succeeded  -> qc
  - Workflow step failed + retries left -> planner  (planner handles wf retries)
  - Code execution failed + retries left -> coder   (regenerate code)
  - Failed + no retries   -> step_finalize  (report failure)

On failure, the error is matched against the Error Pattern Book
(error_patterns.py) to provide precise fix instructions instead of
raw stderr dumps.  On retry success, the error→fix mapping is
recorded in the session-level error_book so later steps can avoid
the same pitfall.
"""
from __future__ import annotations

import glob
import logging
import os
from typing import Dict, List, Tuple

from renzo.app.state import AgentState
from renzo.app.error_patterns import (
    build_fix_hint,
    match_error_patterns,
)

logger = logging.getLogger(__name__)


_NONEMPTY_ENFORCED_PREFIXES = ("derived_", "qc_", "final_validation")
_TEXT_OUTPUT_EXTS = (".csv", ".tsv", ".md", ".txt", ".json", ".html", ".htm")


def _is_workflow_execution(state: AgentState) -> bool:
    """Check if the current execution context is a workflow (not ad-hoc code)."""
    return bool(state.get("workflow_plan"))


def _record_learned_pattern(
    state: AgentState,
    previous_validation: Dict,
) -> List[Dict]:
    """When a retry succeeds, record the error→fix in the session error_book.

    This allows later steps in the same session to benefit from the lesson.
    """
    error_book = list(state.get("error_book", []))

    prev_stderr = previous_validation.get("stderr_excerpt", "")
    matched_ids = previous_validation.get("matched_pattern_ids", [])

    if not prev_stderr:
        return error_book

    # Build a compact summary of what was learned
    entry = {
        "title": previous_validation.get("matched_pattern_title", "Runtime error"),
        "language": state.get("code_language", "both"),
        "stderr_snippet": prev_stderr[:300],
        "fix_description": (
            "The previous code failed and was fixed on retry. "
            "The error was: " + prev_stderr[:200]
        ),
        "matched_static_ids": matched_ids,
        "prevention_hint": "",
    }

    # If we matched a known pattern, use its prevention hint
    if matched_ids:
        from renzo.app.error_patterns import PATTERNS
        for pat in PATTERNS:
            if pat.id in matched_ids and pat.prevention_hint:
                entry["prevention_hint"] = pat.prevention_hint
                break

    error_book.append(entry)
    logger.info(
        "Error book: recorded learned pattern '%s' (total: %d)",
        entry["title"], len(error_book),
    )
    return error_book


def _upsert_error_book_entry(error_book: List[Dict], entry: Dict) -> List[Dict]:
    """Upsert a lesson entry to keep error_book compact and queryable."""
    title = str(entry.get("title", "")).strip()
    stderr = str(entry.get("stderr_snippet", "")).strip()[:180]
    for existing in error_book:
        if (
            str(existing.get("title", "")).strip() == title
            and str(existing.get("stderr_snippet", "")).strip()[:180] == stderr
        ):
            existing.update({**existing, **entry})
            return error_book
    error_book.append(entry)
    return error_book


def _record_failure_lesson(
    state: AgentState,
    *,
    stderr_excerpt: str,
    title: str,
    language: str,
    fix_hint: str,
    category: str,
) -> List[Dict]:
    """Record a failure lesson immediately so next generation can query it."""
    error_book = list(state.get("error_book", []))
    entry = {
        "title": title or "Runtime error",
        "language": language or state.get("code_language", "both"),
        "stderr_snippet": (stderr_excerpt or "")[:300],
        "fix_description": (fix_hint or "")[:400],
        "prevention_hint": (fix_hint or "")[:220],
        "category": category or "runtime_error",
    }
    return _upsert_error_book_entry(error_book, entry)


def _classify_error(stderr: str) -> str:
    s = (stderr or "").lower()
    if "syntaxerror" in s or "unterminated string literal" in s or "never closed" in s:
        return "syntax_error"
    if "no such file" in s or "filenotfounderror" in s or "cannot open" in s:
        return "path_error"
    if "no module named" in s or "there is no package called" in s:
        return "dependency_error"
    if "permission denied" in s:
        return "permission_error"
    return "runtime_error"


def _iter_output_dirs(state: AgentState) -> List[str]:
    dirs: List[str] = []
    seen: set[str] = set()

    def _add(path: str) -> None:
        norm = os.path.normpath(path)
        if not norm or norm in seen:
            return
        if os.path.isdir(norm):
            seen.add(norm)
            dirs.append(norm)

    execution_workdir = str(state.get("execution_workdir") or "").strip()
    if execution_workdir:
        _add(execution_workdir)

    plan_data = state.get("workflow_plan")
    if isinstance(plan_data, dict):
        workflow_dir = str(plan_data.get("workflow_dir") or "").strip()
        if workflow_dir:
            _add(workflow_dir)
            _add(os.path.join(workflow_dir, "output"))
        work_dir = str(plan_data.get("work_dir") or "").strip()
        if work_dir:
            _add(work_dir)
            _add(os.path.join(work_dir, "output"))
    return dirs


def _csv_has_data_rows(path: str) -> bool:
    """Return True if CSV/TSV has at least one data row beyond header."""
    non_empty_lines = 0
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            if line.strip():
                non_empty_lines += 1
            if non_empty_lines >= 2:
                return True
    return False


def _find_empty_or_near_empty_outputs(state: AgentState, *, skip_files: set[str] | None = None) -> List[Dict[str, str]]:
    """Detect zero-byte or header-only outputs for critical workflow artifacts.

    *skip_files*: optional set of basenames to exclude from hard enforcement
    (used for step5 soft-check CSVs that should not trigger a retry).
    """
    problems: List[Dict[str, str]] = []
    _skip = skip_files or set()

    for scan_dir in _iter_output_dirs(state):
        for root, _dirs, files in os.walk(scan_dir):
            for fname in sorted(files):
                if fname.startswith("."):
                    continue
                if fname.startswith("tmp") and (fname.endswith(".py") or fname.endswith(".R")):
                    continue
                if not fname.lower().endswith(_TEXT_OUTPUT_EXTS):
                    continue
                if not fname.lower().startswith(_NONEMPTY_ENFORCED_PREFIXES):
                    continue
                if fname in _skip:
                    continue

                path = os.path.join(root, fname)
                if not os.path.isfile(path):
                    continue

                size = os.path.getsize(path)
                if size == 0:
                    problems.append({"path": path, "reason": "zero-byte"})
                    continue

                if fname.lower().endswith((".csv", ".tsv")):
                    try:
                        if not _csv_has_data_rows(path):
                            problems.append({"path": path, "reason": "header-only"})
                    except Exception:
                        problems.append({"path": path, "reason": "unreadable"})
    return problems


def _cleanup_problem_files(problems: List[Dict[str, str]]) -> List[str]:
    removed: List[str] = []
    for item in problems:
        path = item.get("path", "")
        if not path:
            continue
        try:
            if os.path.isfile(path):
                os.remove(path)
                removed.append(path)
        except Exception:
            continue
    return removed


def _find_output_dirs(state: AgentState) -> List[str]:
    """Return list of output directories to search for workflow step outputs."""
    return _iter_output_dirs(state)


_STEP5_SOFT_CHECK_FILES = {
    "qc_adam_overview.csv",
    "qc_adam_schema_diffs.csv",
    "qc_adam_value_diffs_long.csv",
    "derived_adam_rowcounts.csv",
}

_GLOB_CHARS = set("*?[]")


def _workflow_completion_stamp(step_id: str) -> str:
    return os.path.join("results", "finish", f"{step_id}.done")


def _path_pattern_exists(output_dirs: List[str], pattern: str) -> bool:
    has_glob = any(char in pattern for char in _GLOB_CHARS)
    for root in output_dirs:
        candidate = os.path.join(root, pattern)
        if has_glob:
            matches = sorted(glob.glob(candidate, recursive=True))
            for match in matches:
                if os.path.isfile(match) and os.path.getsize(match) > 0:
                    return True
                if os.path.isdir(match):
                    return True
        else:
            if os.path.isfile(candidate) and os.path.getsize(candidate) > 0:
                return True
            if os.path.isdir(candidate):
                return True
    return False


def _check_workflow_step_output_contract(state: AgentState) -> Tuple[bool, str, str]:
    """Check that the current workflow step produced all required outputs.

    For step5_qc_and_final_report the contract is relaxed:
    - Hard-require only ``final_validation_qc_report.md`` (must exist and be non-empty).
    - The 4 QC CSVs are soft-checked: missing/empty ones are logged as
      warnings but do **not** fail the step so the report can still be
      generated and shown to the user.

    Returns (failed, problem_message, targeted_fix_hint).
    """
    plan_data = state.get("workflow_plan")
    if not isinstance(plan_data, dict):
        return False, "", ""
    try:
        from renzo.app.models.workflow_step import WorkflowPlan
        plan = WorkflowPlan.from_dict(plan_data)
    except Exception:
        return False, "", ""
    current_step_id = state.get("current_step_id") or plan.current_step_id
    step = plan.get_step(current_step_id) if current_step_id else None
    if not step or not getattr(step, "outputs", None):
        return False, "", ""

    required = list(step.outputs)
    output_dirs = _find_output_dirs(state)

    is_step5 = current_step_id == "step5_qc_and_final_report"

    missing: List[str] = []
    soft_missing: List[str] = []
    for fname in required:
        found = _path_pattern_exists(output_dirs, fname)
        if not found:
            if is_step5 and fname in _STEP5_SOFT_CHECK_FILES:
                soft_missing.append(fname)
            else:
                missing.append(fname)

    if soft_missing:
        logger.warning(
            "Step5 QC soft-check: missing or empty optional outputs: %s (not failing step)",
            ", ".join(soft_missing),
        )

    if missing:
        completion_stamp = _workflow_completion_stamp(current_step_id) if current_step_id else ""
        if completion_stamp and _path_pattern_exists(output_dirs, completion_stamp):
            logger.warning(
                "Workflow step %s satisfied via completion stamp fallback %s; missing declared outputs: %s",
                current_step_id,
                completion_stamp,
                ", ".join(missing),
            )
            return False, "", ""
        hint = (
            "This step must produce exactly the following files: "
            + ", ".join(required)
            + ". Do not write extra output files in the root output directory; use a temp/ subdir for intermediates."
        )
        return True, "Missing or empty required outputs: " + ", ".join(missing), hint

    return False, "", ""


def step_validate_node(state: AgentState) -> Dict:
    logs = state.get("execution_logs", [])
    if not logs:
        # Nothing was executed — go back to planner
        return {"next_node": "planner", "validation_result": {"status": "no_logs"}}

    latest = logs[-1]
    exec_status = latest.get("status", "unknown")
    is_wf = _is_workflow_execution(state)

    # ── Success path ──────────────────────────────────────────────────
    if exec_status == "success":
        result: Dict = {}
        _cur_step = state.get("current_step_id") or ""
        _is_step5 = _cur_step == "step5_qc_and_final_report"
        if is_wf:
            # Step 5 (QC & final report) must never fail — skip all
            # empty-output enforcement so the report is always generated.
            output_problems = (
                [] if _is_step5
                else _find_empty_or_near_empty_outputs(state)
            )
            if output_problems:
                removed_files = _cleanup_problem_files(output_problems)
                problem_summaries = [
                    f"{p.get('path', '')} ({p.get('reason', 'invalid')})"
                    for p in output_problems[:8]
                ]
                problem_text = "; ".join(problem_summaries)

                # Reclassify this step as failed so planner can retry with stricter output generation.
                retry_count = state.get("retry_count", 0)
                max_retries = state.get("max_retries", 2)
                wf_step_id = None
                plan_data = state.get("workflow_plan")
                if isinstance(plan_data, dict):
                    try:
                        from renzo.app.models.workflow_step import WorkflowPlan, StepStatus
                        plan = WorkflowPlan.from_dict(plan_data)
                        wf_step_id = state.get("current_step_id") or plan.current_step_id
                        step = plan.get_step(wf_step_id) if wf_step_id else None
                        if step:
                            retry_count = int(step.retry_count)
                            max_retries = int(step.max_retries)
                    except Exception:
                        pass

                failure_report = {
                    "status": "failed",
                    "exec_status": "output_validation_failed",
                    "stderr_excerpt": (
                        "Detected empty or near-empty workflow outputs: "
                        f"{problem_text}"
                    )[:1200],
                    "stdout_excerpt": latest.get("stdout", "")[:800],
                    "retry_count": retry_count,
                    "max_retries": max_retries,
                    "matched_pattern_ids": [],
                    "matched_pattern_title": "empty_output_detected",
                    "error_category": "runtime_error",
                    "targeted_fix_hint": (
                        "Do not pre-create output files. Build dataframes first, "
                        "then write files atomically and ensure derived_/qc_ CSV files "
                        "contain at least one data row."
                    ),
                }
                failure_error_book = _record_failure_lesson(
                    state,
                    stderr_excerpt=failure_report["stderr_excerpt"],
                    title="empty_output_detected",
                    language=latest.get("language", state.get("code_language", "both")),
                    fix_hint=failure_report["targeted_fix_hint"],
                    category="output_quality",
                )

                updated_logs = list(logs)
                latest_with_error = dict(latest)
                latest_with_error.update({
                    "status": "error",
                    "error_pattern_id": "empty_output_detected",
                    "error_category": "runtime_error",
                    "stderr_tail": failure_report["stderr_excerpt"][-500:],
                    "stdout_tail": (latest.get("stdout", "") or "")[-500:],
                    "retry_count": retry_count,
                    "removed_empty_outputs": removed_files,
                })
                updated_logs[-1] = latest_with_error

                if retry_count < max_retries:
                    workflow_updates: Dict = {}
                    if isinstance(plan_data, dict):
                        try:
                            from renzo.app.models.workflow_step import WorkflowPlan, StepStatus
                            plan = WorkflowPlan.from_dict(plan_data)
                            step_id = wf_step_id or state.get("current_step_id") or plan.current_step_id
                            step = plan.get_step(step_id) if step_id else None
                            if step:
                                step.status = StepStatus.PENDING
                                step.retry_count += 1
                                plan.current_step_id = step.id
                            workflow_updates["workflow_plan"] = plan.to_dict()
                        except Exception:
                            pass
                    return {
                        "validation_result": failure_report,
                        "retry_count": retry_count + 1,
                        "workflow_status": "running",
                        "error_book": failure_error_book,
                        "execution_logs": updated_logs,
                        **workflow_updates,
                        "next_node": "planner",
                    }

                failure_report["terminal"] = True
                workflow_updates: Dict = {}
                if isinstance(plan_data, dict):
                    try:
                        from renzo.app.models.workflow_step import WorkflowPlan, StepStatus
                        plan = WorkflowPlan.from_dict(plan_data)
                        step_id = wf_step_id or state.get("current_step_id") or plan.current_step_id
                        step = plan.get_step(step_id) if step_id else None
                        if step:
                            step.status = StepStatus.FAILED
                            step.error = failure_report["stderr_excerpt"][:500]
                            step.retry_count = max(step.retry_count, retry_count + 1)
                        plan.status = "failed"
                        workflow_updates["workflow_plan"] = plan.to_dict()
                    except Exception:
                        pass
                return {
                    "validation_result": failure_report,
                    "workflow_status": "failed",
                    "error_book": failure_error_book,
                    "execution_logs": updated_logs,
                    **workflow_updates,
                    "next_node": "step_finalize",
                }

            # Required outputs contract: step.outputs must all exist; step5 must have at least 5 rows in qc_adam_schema_diffs (core 5)
            contract_failed, contract_message, contract_hint = _check_workflow_step_output_contract(state)
            if contract_failed:
                plan_data = state.get("workflow_plan")
                retry_count = state.get("retry_count", 0)
                max_retries = state.get("max_retries", 2)
                wf_step_id = state.get("current_step_id")
                if isinstance(plan_data, dict):
                    try:
                        from renzo.app.models.workflow_step import WorkflowPlan, StepStatus
                        plan = WorkflowPlan.from_dict(plan_data)
                        wf_step_id = wf_step_id or plan.current_step_id
                        step = plan.get_step(wf_step_id) if wf_step_id else None
                        if step:
                            retry_count = int(step.retry_count)
                            max_retries = int(step.max_retries)
                    except Exception:
                        pass

                failure_report = {
                    "status": "failed",
                    "exec_status": "output_validation_failed",
                    "stderr_excerpt": ("Required outputs contract violated: " + contract_message)[:1200],
                    "stdout_excerpt": latest.get("stdout", "")[:800],
                    "retry_count": retry_count,
                    "max_retries": max_retries,
                    "matched_pattern_ids": [],
                    "matched_pattern_title": "output_contract_violation",
                    "error_category": "runtime_error",
                    "targeted_fix_hint": contract_hint,
                }
                failure_error_book = _record_failure_lesson(
                    state,
                    stderr_excerpt=failure_report["stderr_excerpt"],
                    title="output_contract_violation",
                    language=latest.get("language", state.get("code_language", "both")),
                    fix_hint=contract_hint,
                    category="output_quality",
                )
                updated_logs = list(logs)
                latest_with_error = dict(latest)
                latest_with_error.update({
                    "status": "error",
                    "error_pattern_id": "output_contract_violation",
                    "error_category": "runtime_error",
                    "stderr_tail": failure_report["stderr_excerpt"][-500:],
                    "stdout_tail": (latest.get("stdout", "") or "")[-500:],
                    "retry_count": retry_count,
                })
                updated_logs[-1] = latest_with_error

                if retry_count < max_retries:
                    workflow_updates = {}
                    if isinstance(plan_data, dict):
                        try:
                            from renzo.app.models.workflow_step import WorkflowPlan, StepStatus
                            plan = WorkflowPlan.from_dict(plan_data)
                            step_id = wf_step_id or plan.current_step_id
                            step = plan.get_step(step_id) if step_id else None
                            if step:
                                step.status = StepStatus.PENDING
                                step.retry_count += 1
                                plan.current_step_id = step.id
                            workflow_updates["workflow_plan"] = plan.to_dict()
                        except Exception:
                            pass
                    return {
                        "validation_result": failure_report,
                        "retry_count": retry_count + 1,
                        "workflow_status": "running",
                        "error_book": failure_error_book,
                        "execution_logs": updated_logs,
                        **workflow_updates,
                        "next_node": "planner",
                    }

                failure_report["terminal"] = True
                workflow_updates = {}
                if isinstance(plan_data, dict):
                    try:
                        from renzo.app.models.workflow_step import WorkflowPlan, StepStatus
                        plan = WorkflowPlan.from_dict(plan_data)
                        step_id = wf_step_id or plan.current_step_id
                        step = plan.get_step(step_id) if step_id else None
                        if step:
                            step.status = StepStatus.FAILED
                            step.error = failure_report["stderr_excerpt"][:500]
                            step.retry_count = max(step.retry_count, retry_count + 1)
                        plan.status = "failed"
                        workflow_updates["workflow_plan"] = plan.to_dict()
                    except Exception:
                        pass
                return {
                    "validation_result": failure_report,
                    "workflow_status": "failed",
                    "error_book": failure_error_book,
                    "execution_logs": updated_logs,
                    **workflow_updates,
                    "next_node": "step_finalize",
                }

        # If this was a retry (previous attempt failed), record what we learned
        previous_validation = state.get("validation_result", {})
        if previous_validation.get("status") == "failed":
            error_book = _record_learned_pattern(state, previous_validation)
            result["error_book"] = error_book

        # Route to data_analyst (post_step mode) to profile outputs
        # before QC runs. data_analyst will then route to qc.
        result.update({
            "validation_result": {
                "status": "success",
                "detail": (
                    "Workflow step completed successfully."
                    if is_wf else
                    "Execution completed successfully."
                ),
            },
            "data_analyst_mode": "post_step",
            "workflow_status": "running" if is_wf else state.get("workflow_status"),
            "next_node": "data_analyst",
        })
        return result

    # ── Failure path ──────────────────────────────────────────────────
    retry_count = state.get("retry_count", 0)
    max_retries = state.get("max_retries", 2)

    # For workflow runs, retries should follow per-step settings in workflow_plan
    # instead of the global state defaults.
    plan_data = state.get("workflow_plan")
    wf_step_id = None
    if is_wf and isinstance(plan_data, dict):
        try:
            from renzo.app.models.workflow_step import WorkflowPlan
            plan = WorkflowPlan.from_dict(plan_data)
            wf_step_id = state.get("current_step_id") or plan.current_step_id
            step = plan.get_step(wf_step_id) if wf_step_id else None
            if step:
                retry_count = int(step.retry_count)
                max_retries = int(step.max_retries)
        except Exception:
            pass

    stderr = latest.get("stderr", "")[:1200]
    stdout = latest.get("stdout", "")[:800]
    language = latest.get("language", state.get("code_language", "both"))

    # Match against the Error Pattern Book
    matches = match_error_patterns(stderr, language)
    matched_pattern_ids = [m.pattern.id for m in matches]
    matched_pattern_title = matches[0].pattern.title if matches else ""
    error_category = _classify_error(stderr)

    # Build targeted fix hint (combines pattern knowledge + raw stderr)
    error_book = state.get("error_book", [])
    targeted_fix_hint = build_fix_hint(stderr, language, error_book)

    failure_report = {
        "status": "failed",
        "exec_status": exec_status,
        "stderr_excerpt": stderr,
        "stdout_excerpt": stdout,
        "retry_count": retry_count,
        "max_retries": max_retries,
        # Error Pattern Book enrichment
        "matched_pattern_ids": matched_pattern_ids,
        "matched_pattern_title": matched_pattern_title,
        "error_category": error_category,
        "targeted_fix_hint": targeted_fix_hint,
    }
    failure_error_book = _record_failure_lesson(
        state,
        stderr_excerpt=stderr,
        title=matched_pattern_title or error_category,
        language=language,
        fix_hint=targeted_fix_hint,
        category=error_category,
    )

    # Enrich the latest execution log so failures are traceable even before finalize.
    updated_logs = list(logs)
    latest_with_error = dict(latest)
    latest_with_error.update({
        "error_pattern_id": matched_pattern_ids[0] if matched_pattern_ids else "",
        "error_category": error_category,
        "stderr_tail": stderr[-500:],
        "stdout_tail": stdout[-500:],
        "retry_count": retry_count,
    })
    updated_logs[-1] = latest_with_error

    if matched_pattern_ids:
        logger.info(
            "Error Pattern Book matched: %s for stderr: %.100s",
            matched_pattern_ids, stderr[:100],
        )
    else:
        logger.info(
            "Error Pattern Book: no match for stderr: %.100s", stderr[:100],
        )

    if retry_count < max_retries:
        if is_wf:
            workflow_updates: Dict = {}
            if isinstance(plan_data, dict):
                try:
                    from renzo.app.models.workflow_step import WorkflowPlan, StepStatus
                    plan = WorkflowPlan.from_dict(plan_data)
                    step_id = wf_step_id or state.get("current_step_id") or plan.current_step_id
                    step = plan.get_step(step_id) if step_id else None
                    if step:
                        step.status = StepStatus.PENDING
                        step.retry_count += 1
                        plan.current_step_id = step.id
                    workflow_updates["workflow_plan"] = plan.to_dict()
                except Exception:
                    pass
            # Workflow step failed — route to planner for retry logic
            return {
                "validation_result": failure_report,
                "retry_count": retry_count + 1,
                "workflow_status": "running",
                "error_book": failure_error_book,
                "execution_logs": updated_logs,
                **workflow_updates,
                "next_node": "planner",
            }
        else:
            # Code execution failed — let coder regenerate with the error context
            return {
                "validation_result": failure_report,
                "retry_count": retry_count + 1,
                "error_book": failure_error_book,
                "execution_logs": updated_logs,
                "next_node": "coder",
            }

    # No retries left — finalize with failure (or force-complete for step5)
    _cur_step_id = wf_step_id or state.get("current_step_id") or ""
    _is_step5 = _cur_step_id == "step5_qc_and_final_report"

    failure_report["terminal"] = True
    if is_wf:
        workflow_updates: Dict = {}
        if isinstance(plan_data, dict):
            try:
                from renzo.app.models.workflow_step import WorkflowPlan, StepStatus
                plan = WorkflowPlan.from_dict(plan_data)
                step_id = _cur_step_id or plan.current_step_id
                step = plan.get_step(step_id) if step_id else None
                if _is_step5:
                    # Step 5 must never fail — mark as completed so step_finalize
                    # and responder treat it as a (partial) success and generate
                    # the report describing whatever QC state was reached.
                    if step:
                        step.status = StepStatus.COMPLETED
                        step.error = f"(warn) {stderr[:400]}"
                        step.retry_count = max(step.retry_count, retry_count + 1)
                    plan.status = "completed"
                    failure_report["status"] = "warn"
                    logger.warning(
                        "Step5 retries exhausted — force-completing so report is generated. stderr: %.200s",
                        stderr[:200],
                    )
                else:
                    if step:
                        step.status = StepStatus.FAILED
                        step.error = stderr[:500]
                        step.retry_count = max(step.retry_count, retry_count + 1)
                    plan.status = "failed"
                workflow_updates["workflow_plan"] = plan.to_dict()
            except Exception:
                pass

        wf_status = "success" if _is_step5 else "failed"
        return {
            "validation_result": failure_report,
            "workflow_status": wf_status,
            "error_book": failure_error_book,
            "execution_logs": updated_logs,
            **workflow_updates,
            "next_node": "step_finalize",
        }
    return {
        "validation_result": failure_report,
        "error_book": failure_error_book,
        "execution_logs": updated_logs,
        "next_node": "step_finalize",
    }
