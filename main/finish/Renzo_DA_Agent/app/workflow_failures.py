from __future__ import annotations

import re
from pathlib import Path
from typing import Any


_FAILURE_RULES = (
    {
        "code": "finish_step_config_error",
        "category": "step_config",
        "retryable": False,
        "summary": "A finish step config referenced template fields that were not available during target expansion.",
        "patterns": ("targets_from_table", "missing placeholder"),
        "hint": "Check the step config pattern against the columns in the referenced TSV file.",
    },
    {
        "code": "conda_prefix_collision",
        "category": "runtime_environment",
        "retryable": True,
        "summary": "Concurrent conda environment creation collided on the same prefix.",
        "patterns": ("prefix record", "already exists"),
        "hint": "Use an isolated Snakemake conda prefix per run or clean the shared prefix before retrying.",
    },
    {
        "code": "snakemake_wrapper_unavailable",
        "category": "source_dependency",
        "retryable": True,
        "summary": "Snakemake could not fetch or locate a remote wrapper.",
        "patterns": ("unable to locate wrapper script", "snakemake-wrappers"),
        "hint": "Reset the Snakemake source cache and retry with stable network access.",
    },
    {
        "code": "snakemake_scheduler_deadlock",
        "category": "workflow_scheduler",
        "retryable": False,
        "summary": "Snakemake reported that jobs remain but none are schedulable.",
        "patterns": ("out of jobs ready to be started",),
        "hint": "Prefer explicit concrete targets over partial `all --until ...` execution for finish steps.",
    },
    {
        "code": "workflow_dependency_missing",
        "category": "dependency",
        "retryable": False,
        "summary": "A required Python or R dependency is missing in the workflow environment.",
        "patterns": ("no module named", "there is no package called"),
        "hint": "Install the missing package in the workflow env or switch to a prepared runtime image.",
    },
    {
        "code": "biomart_service_unavailable",
        "category": "network",
        "retryable": True,
        "summary": "The remote BioMart service was temporarily unavailable.",
        "patterns": ("biomart::exception::database", "can't connect to mysql server"),
        "hint": "Retry after a short delay; this is usually a transient remote service failure.",
    },
    {
        "code": "workflow_network_failure",
        "category": "network",
        "retryable": True,
        "summary": "Workflow execution failed while accessing a remote network resource.",
        "patterns": ("temporary failure in name resolution", "connection timed out", "failed to connect", "could not resolve host"),
        "hint": "Retry after restoring outbound network access.",
    },
    {
        "code": "workflow_subprocess_failed",
        "category": "runtime_error",
        "retryable": False,
        "summary": "A nested workflow subprocess exited with a non-zero status.",
        "patterns": ("returned non-zero exit status",),
        "hint": "Inspect the referenced rule log for the underlying tool failure.",
    },
)


_LOG_LINE_RE = re.compile(r"log:\s*([^\n]+)")


def _referenced_log_paths(stderr: str) -> list[str]:
    paths: list[str] = []
    for match in _LOG_LINE_RE.finditer(stderr or ""):
        raw = match.group(1).split("(", 1)[0]
        for item in raw.split(","):
            text = item.strip()
            if text:
                paths.append(text)
    return paths


def _referenced_logs_tail(stderr: str, work_dir: str | Path | None, limit: int = 2000) -> str:
    if not work_dir:
        return ""
    base = Path(work_dir).resolve()
    chunks: list[str] = []
    for raw_path in _referenced_log_paths(stderr):
        path = Path(raw_path)
        resolved = path if path.is_absolute() else (base / path)
        if not resolved.exists() or not resolved.is_file():
            continue
        try:
            chunks.append(f"\n[log tail: {raw_path}]\n{resolved.read_text(encoding='utf-8', errors='replace')[-limit:]}")
        except Exception:
            continue
    return "\n".join(chunks)


def classify_workflow_failure(stdout: str = "", stderr: str = "", *, work_dir: str | Path | None = None) -> dict[str, Any]:
    text = f"{stdout or ''}\n{stderr or ''}"
    text = f"{text}\n{_referenced_logs_tail(stderr, work_dir)}"
    lowered = text.lower()
    for rule in _FAILURE_RULES:
        if all(pattern in lowered for pattern in rule["patterns"]):
            return {
                "code": rule["code"],
                "category": rule["category"],
                "retryable": rule["retryable"],
                "summary": rule["summary"],
                "hint": rule["hint"],
            }
    return {
        "code": "workflow_runtime_error",
        "category": "runtime_error",
        "retryable": False,
        "summary": "Workflow execution failed with an unclassified runtime error.",
        "hint": "Inspect stderr_tail for the underlying tool or workflow failure.",
    }
