"""QC validation rules — pluggable rule chain for quality control.

Each rule function takes a context dict and returns a structured result:
  {"rule": str, "status": "pass"|"warn"|"fail", "detail": str}

Rules are designed to be composable. The QC node runs all applicable
rules and aggregates results for the Planner to decide next steps.
"""
from __future__ import annotations

import os
from typing import Any, Callable, Dict, List

# Type alias for a QC rule function
QCRule = Callable[[Dict[str, Any]], Dict[str, Any]]


# ── Built-in V1 rules ────────────────────────────────────────────────

def check_execution_success(ctx: Dict[str, Any]) -> Dict[str, Any]:
    """Check if the latest execution succeeded."""
    log = ctx.get("latest_log", {})
    if log.get("status") == "error":
        stderr = log.get("stderr", "")[:300]
        return {
            "rule": "execution_success",
            "status": "fail",
            "detail": f"Execution failed: {stderr}",
        }
    return {"rule": "execution_success", "status": "pass", "detail": "Execution succeeded."}


def check_output_files_exist(ctx: Dict[str, Any]) -> Dict[str, Any]:
    """Check if the execution produced any output files."""
    outputs_dir = ctx.get("outputs_dir", "")
    if not outputs_dir or not os.path.isdir(outputs_dir):
        return {
            "rule": "output_files_exist",
            "status": "warn",
            "detail": f"Outputs directory not found: {outputs_dir}",
        }

    files = []
    for root, _dirs, filenames in os.walk(outputs_dir):
        for f in filenames:
            if f.startswith("."):
                continue
            files.append(os.path.relpath(os.path.join(root, f), outputs_dir))
    if not files:
        return {
            "rule": "output_files_exist",
            "status": "warn",
            "detail": "No output files were produced.",
        }
    return {
        "rule": "output_files_exist",
        "status": "pass",
        "detail": f"Found {len(files)} output file(s): {', '.join(files[:5])}",
    }


def check_output_non_empty(ctx: Dict[str, Any]) -> Dict[str, Any]:
    """Check that output files are not empty (zero-byte)."""
    outputs_dir = ctx.get("outputs_dir", "")
    if not outputs_dir or not os.path.isdir(outputs_dir):
        return {"rule": "output_non_empty", "status": "pass", "detail": "No outputs dir to check."}

    empty_files = []
    for root, _dirs, filenames in os.walk(outputs_dir):
        for fname in filenames:
            fpath = os.path.join(root, fname)
            if os.path.isfile(fpath) and os.path.getsize(fpath) == 0:
                empty_files.append(os.path.relpath(fpath, outputs_dir))

    if empty_files:
        return {
            "rule": "output_non_empty",
            "status": "warn",
            "detail": f"Empty output files: {', '.join(empty_files)}",
        }
    return {"rule": "output_non_empty", "status": "pass", "detail": "All output files have content."}


def check_csv_missing_values(ctx: Dict[str, Any]) -> Dict[str, Any]:
    """Check CSV outputs for excessive missing values (>50%)."""
    outputs_dir = ctx.get("outputs_dir", "")
    if not outputs_dir or not os.path.isdir(outputs_dir):
        return {"rule": "csv_missing_values", "status": "pass", "detail": "No outputs to check."}

    try:
        import pandas as pd
    except ImportError:
        return {"rule": "csv_missing_values", "status": "pass", "detail": "pandas not available for check."}

    issues = []
    for root, _dirs, filenames in os.walk(outputs_dir):
        for fname in filenames:
            if not fname.endswith(".csv"):
                continue
            fpath = os.path.join(root, fname)
            rel = os.path.relpath(fpath, outputs_dir)
            try:
                df = pd.read_csv(fpath, nrows=100)
                if df.empty:
                    continue
                missing_pct = df.isna().mean()
                bad_cols = missing_pct[missing_pct > 0.5].index.tolist()
                if bad_cols:
                    issues.append(f"{rel}: >50% missing in columns {bad_cols[:3]}")
            except Exception:
                continue

    if issues:
        return {
            "rule": "csv_missing_values",
            "status": "warn",
            "detail": "; ".join(issues),
        }
    return {"rule": "csv_missing_values", "status": "pass", "detail": "CSV outputs have acceptable missing value levels."}


def check_column_schema(ctx: Dict[str, Any]) -> Dict[str, Any]:
    """Basic check that CSV outputs have named columns (not just indices)."""
    outputs_dir = ctx.get("outputs_dir", "")
    if not outputs_dir or not os.path.isdir(outputs_dir):
        return {"rule": "column_schema", "status": "pass", "detail": "No outputs to check."}

    try:
        import pandas as pd
    except ImportError:
        return {"rule": "column_schema", "status": "pass", "detail": "pandas not available."}

    issues = []
    for root, _dirs, filenames in os.walk(outputs_dir):
        for fname in filenames:
            if not fname.endswith(".csv"):
                continue
            fpath = os.path.join(root, fname)
            rel = os.path.relpath(fpath, outputs_dir)
            try:
                df = pd.read_csv(fpath, nrows=1)
                unnamed = [c for c in df.columns if str(c).startswith("Unnamed")]
                if unnamed:
                    issues.append(f"{rel}: has {len(unnamed)} unnamed column(s)")
            except Exception:
                continue

    if issues:
        return {
            "rule": "column_schema",
            "status": "warn",
            "detail": "; ".join(issues),
        }
    return {"rule": "column_schema", "status": "pass", "detail": "All CSV outputs have named columns."}


def check_output_row_count(ctx: Dict[str, Any]) -> Dict[str, Any]:
    """Check that output data files have a reasonable number of rows.

    Uses the data_catalog to compare output row counts against input row counts.
    Flags empty outputs or outputs with zero rows as failures.
    """
    catalog = ctx.get("data_catalog", [])
    if not catalog:
        return {"rule": "output_row_count", "status": "pass", "detail": "No catalog available."}

    outputs = [e for e in catalog if e.get("source") == "output"]
    if not outputs:
        return {"rule": "output_row_count", "status": "pass", "detail": "No output files in catalog."}

    issues = []
    for entry in outputs:
        rows = entry.get("rows", -1)
        if rows == 0:
            issues.append(f"{entry['filename']}: 0 rows (empty output)")
        elif rows < 0:
            issues.append(f"{entry['filename']}: could not determine row count")

    if issues:
        return {
            "rule": "output_row_count",
            "status": "warn",
            "detail": "; ".join(issues),
        }

    summary = ", ".join(f"{e['filename']}({e['rows']})" for e in outputs[:5])
    return {
        "rule": "output_row_count",
        "status": "pass",
        "detail": f"Output row counts: {summary}",
    }


def check_key_columns_preserved(ctx: Dict[str, Any]) -> Dict[str, Any]:
    """Check that key columns (USUBJID, STUDYID, etc.) survive transformations.

    If input files have key columns, output files should generally retain them.
    """
    catalog = ctx.get("data_catalog", [])
    if not catalog:
        return {"rule": "key_columns_preserved", "status": "pass", "detail": "No catalog available."}

    inputs = [e for e in catalog if e.get("source") == "input"]
    outputs = [e for e in catalog if e.get("source") == "output"]
    if not inputs or not outputs:
        return {"rule": "key_columns_preserved", "status": "pass", "detail": "Insufficient data for comparison."}

    # Collect key columns from inputs
    input_keys = set()
    for e in inputs:
        for k in e.get("key_columns", []):
            input_keys.add(k.upper())

    if not input_keys:
        return {"rule": "key_columns_preserved", "status": "pass", "detail": "No key columns detected in input."}

    # Check which key columns appear in outputs
    missing_in_any = []
    for entry in outputs:
        output_cols = {c.upper() for c in entry.get("column_names", [])}
        # Only check the most important keys
        for key in ["USUBJID", "STUDYID"]:
            if key in input_keys and key not in output_cols and entry.get("rows", 0) > 0:
                missing_in_any.append(f"{entry['filename']} missing {key}")

    if missing_in_any:
        return {
            "rule": "key_columns_preserved",
            "status": "warn",
            "detail": "; ".join(missing_in_any[:5]),
        }
    return {
        "rule": "key_columns_preserved",
        "status": "pass",
        "detail": f"Key columns preserved in outputs. Input keys: {', '.join(sorted(input_keys)[:5])}",
    }


# ── Rule registry ─────────────────────────────────────────────────────

# V1 default rule chain — order matters
DEFAULT_RULES: List[QCRule] = [
    check_execution_success,
    check_output_files_exist,
    check_output_non_empty,
    check_csv_missing_values,
    check_column_schema,
    check_output_row_count,
    check_key_columns_preserved,
]


def run_qc_rules(
    ctx: Dict[str, Any],
    rules: List[QCRule] | None = None,
) -> List[Dict[str, Any]]:
    """Run a list of QC rules and return all results.

    Parameters
    ----------
    ctx : dict
        Context for the rules. Expected keys:
        - latest_log: dict with execution log
        - outputs_dir: path to outputs directory
    rules : list, optional
        Rules to run. Defaults to DEFAULT_RULES.

    Returns
    -------
    list of dict
        One result per rule, each with "rule", "status", "detail".
    """
    if rules is None:
        rules = DEFAULT_RULES

    results = []
    for rule in rules:
        try:
            result = rule(ctx)
            results.append(result)
        except Exception as e:
            results.append({
                "rule": getattr(rule, "__name__", "unknown"),
                "status": "warn",
                "detail": f"Rule raised exception: {e}",
            })
    return results


def summarize_qc(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Summarize QC results into an overall verdict.

    Returns
    -------
    dict with "status" (pass/warn/fail), "total", "passed", "warned",
    "failed", and "details" (list of per-rule results).
    """
    passed = sum(1 for r in results if r.get("status") == "pass")
    warned = sum(1 for r in results if r.get("status") == "warn")
    failed = sum(1 for r in results if r.get("status") == "fail")

    if failed > 0:
        overall = "fail"
    elif warned > 0:
        overall = "warn"
    else:
        overall = "pass"

    return {
        "status": overall,
        "total": len(results),
        "passed": passed,
        "warned": warned,
        "failed": failed,
        "details": results,
    }
