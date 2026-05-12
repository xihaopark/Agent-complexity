"""V3 insight layer: turn V2 per-task scores into a diagnostic object.

The insight block explains *why* an output passes or fails.  It is pure
post-processing on top of a V2 task record (`per_file`, `process_signals`,
`process_counts`) plus a re-read of the run's ``trajectory.jsonl``.

Fields produced per task:

* ``failure_mode`` - one of the enumerated strings (see rubric).
* ``differential`` - one short note per expected file.
* ``skill_tokens_matched`` - subset of the arm's skill tokens that show up
  in at least one trajectory tool-call argument string.
* ``actionable_fix`` - a one-liner keyed on ``failure_mode``.
* ``confidence`` - ``high`` / ``medium`` / ``low``.

All logic is deterministic; no LLM calls.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


_RDS_EXT = {".rds"}


# ---------------------------------------------------------------------------
# Trajectory replay
# ---------------------------------------------------------------------------


def _iter_steps(trajectory_path: Path):
    try:
        with trajectory_path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except Exception:
                    continue
                if isinstance(obj, dict):
                    yield obj
    except FileNotFoundError:
        return


def _tool_calls(step: dict):
    action = step.get("action") or {}
    value = action.get("value") if isinstance(action, dict) else None
    if not isinstance(value, dict):
        return
    for call in value.get("tool_calls") or []:
        fn = (call or {}).get("function") or {}
        name = fn.get("name")
        raw_args = fn.get("arguments")
        if isinstance(raw_args, str):
            args_str = raw_args
        elif isinstance(raw_args, dict):
            try:
                args_str = json.dumps(raw_args, default=str)
            except Exception:
                args_str = str(raw_args)
        else:
            args_str = ""
        if name:
            yield name, args_str


def _tool_obs(step: dict):
    for key in ("next_observation", "observation"):
        obs = step.get(key) or []
        if not isinstance(obs, list):
            continue
        for item in obs:
            if isinstance(item, dict) and item.get("role") == "tool":
                yield item.get("name"), str(item.get("content") or "")


def scan_trajectory(trajectory_path: Path, skill_tokens: list[str]) -> dict:
    """Replay the trajectory once and harvest V3-specific signals."""
    lowered_tokens = [(t, t.lower()) for t in skill_tokens if t]

    steps_total = 0
    first_write_step: int | None = None
    writes_after_first: int = 0
    rscript_errs: list[str] = []
    matched_tokens: set[str] = set()
    all_tool_args_lower: list[str] = []

    for step in _iter_steps(trajectory_path):
        steps_total += 1
        idx = step.get("timestep", steps_total - 1)
        for name, args_str in _tool_calls(step):
            low = args_str.lower()
            all_tool_args_lower.append(low)
            for tok, tok_lower in lowered_tokens:
                if tok_lower in low:
                    matched_tokens.add(tok)
            if name in {"write_text_file", "run_rscript"}:
                if first_write_step is None:
                    first_write_step = idx
                else:
                    writes_after_first += 1
        for tool_name, content in _tool_obs(step):
            if tool_name == "run_rscript" or (tool_name == "run_shell" and "rscript" in content.lower()[:256]):
                if re.search(r"(?i)(Execution halted|(^|\n)Error\s|traceback:)", content):
                    snippet = ""
                    for line in content.splitlines():
                        if line.strip().lower().startswith("error") or "execution halted" in line.lower():
                            snippet = line.strip()
                            break
                    if not snippet:
                        snippet = content.strip().splitlines()[-1][:160] if content.strip() else "(empty)"
                    rscript_errs.append(snippet[:160])

    return {
        "steps_total": steps_total,
        "first_write_step": first_write_step,
        "writes_after_first": writes_after_first,
        "rscript_errs": rscript_errs,
        "skill_tokens_matched": sorted(matched_tokens),
    }


# ---------------------------------------------------------------------------
# Differential diff + per-file mode
# ---------------------------------------------------------------------------


def _jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 1.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


def per_file_diff_note(fs: dict) -> str:
    """One-line human diff for a single expected file, ≤ 120 chars."""
    strat = fs.get("strategy_used", "")
    score = fs.get("strategy_score", 0.0)
    bytes_eq = fs.get("bytes_identical", False)
    size_a = fs.get("size_agent")
    size_r = fs.get("size_ref")
    details = fs.get("details") or {}
    tab = details.get("tabular") or {}

    if strat == "missing":
        return "file missing"
    if strat == "missing_reference":
        return "reference file missing on disk (cannot compare)"
    if bytes_eq:
        return "byte-identical"
    if strat in {"normalized_text_equal", "normalized_table_equal", "rds_normalized_equal",
                 "text_equal", "text_equal_json"}:
        return f"tolerant equal ({strat})"
    if tab:
        cols_a = tab.get("cols_a", 0)
        cols_b = tab.get("cols_b", 0)
        shared = tab.get("cols_shared", 0)
        rows_a = tab.get("rows_a", 0)
        rows_b = tab.get("rows_b", 0)
        cells_total = tab.get("cells_total", 0) or 0
        cells_matched = tab.get("cells_matched", 0) or 0
        cell_frac = tab.get("cell_match_fraction", 0.0)
        row_frac = tab.get("row_match_fraction", 0.0)
        cols_mismatch = tab.get("cols_mismatch", False)
        if cols_mismatch:
            return f"column count {cols_a} vs ref {cols_b} (shared {shared})"[:120]
        if rows_a != rows_b:
            return f"row count {rows_a} vs ref {rows_b} ({abs(rows_a - rows_b)} diff), cells≈{cell_frac:.2f}"[:120]
        if cells_total and cells_matched / cells_total >= 0.95:
            return f"≥95% cells equal under tolerance (float drift; score {score:.2f})"[:120]
        if row_frac >= 0.8:
            return f"rows reshuffled but {row_frac*100:.0f}% content matches (score {score:.2f})"[:120]
        return f"schema-aligned, cells {cell_frac*100:.0f}%, rows {row_frac*100:.0f}% (score {score:.2f})"[:120]
    if strat == "rds_semantic":
        return f"rds sidecar OK, tabular drift (score {score:.2f})"
    if strat == "process_credit":
        if size_a and size_r:
            return f"file present {size_a}B vs ref {size_r}B, unparseable by V2 ladder (process credit 0.25)"[:120]
        return "file present but unparseable by V2 ladder (process credit 0.25)"
    if strat == "fail" or score == 0.0:
        if size_a is not None:
            return f"produced {size_a}B but no tier matched"[:120]
        return "no tier matched"
    return f"{strat} score={score:.2f}"[:120]


def _classify_file_mode(fs: dict) -> str:
    strat = fs.get("strategy_used", "")
    score = fs.get("strategy_score", 0.0)
    bytes_eq = fs.get("bytes_identical", False)
    details = fs.get("details") or {}
    tab = details.get("tabular") or {}
    rds_diag = details.get("rds_diag") or {}
    filename = fs.get("filename") or ""
    is_rds = any(filename.lower().endswith(ext) for ext in _RDS_EXT)

    if bytes_eq or score >= 0.99:
        return "ok"
    if strat == "missing":
        return "output_missing"
    if strat == "missing_reference":
        return "missing_reference"

    if tab:
        cols_a = tab.get("cols_a", 0)
        cols_b = tab.get("cols_b", 0)
        cols_mismatch = tab.get("cols_mismatch", False)
        cells_total = tab.get("cells_total", 0) or 0
        cells_matched = tab.get("cells_matched", 0) or 0
        cell_frac = tab.get("cell_match_fraction", 0.0)
        # Column-level schema drift
        if cols_mismatch:
            return "schema_drift"
        # Same column count, different cells
        if cells_total and cells_matched / cells_total >= 0.95:
            return "float_drift"
        if cells_total and cells_matched < 0.8 * cells_total:
            return "row_drift"
        return "row_drift"

    if is_rds or strat == "rds_semantic" or rds_diag:
        return "rds_semantic_gap"

    if strat == "process_credit":
        return "row_drift"  # file present but can't parse tier: treat as content drift
    if strat == "fail":
        return "schema_drift"
    return "unknown"


def classify_task_failure_mode(
    task_result: dict,
    traj_info: dict,
    *,
    min_steps_for_loop: int = 8,
) -> str:
    verdict = task_result.get("verdict", "fail")
    if verdict == "pass":
        return "ok"

    process = task_result.get("process_signals") or {}
    counts = task_result.get("process_counts") or {}
    rscript_ok_flag = process.get("rscript_invoked_and_exited_zero", 0.0) >= 1.0
    meaningful_count = counts.get("tool_calls_meaningful", 0)
    rscript_err_count = counts.get("rscript_err", 0)
    per_file = task_result.get("per_file") or []
    any_output = any((fs.get("size_agent") or 0) > 0 for fs in per_file)

    if (not rscript_ok_flag) and meaningful_count <= 2 and not any_output:
        return "no_rscript_call"
    if rscript_err_count >= 1 and not any_output:
        return "rscript_crashed"

    # Infinite debug loop: lots of attempts but no file success and lots of steps after first write.
    steps_total = traj_info.get("steps_total", 0)
    writes_after_first = traj_info.get("writes_after_first", 0)
    if (
        steps_total >= min_steps_for_loop
        and writes_after_first >= min_steps_for_loop - 1
        and not any(_classify_file_mode(fs) == "ok" for fs in per_file)
    ):
        return "infinite_debug_loop"

    # Per-file modes
    file_modes = [_classify_file_mode(fs) for fs in per_file]
    file_modes_nontrivial = [m for m in file_modes if m not in {"ok", "missing_reference"}]

    if not file_modes_nontrivial:
        return "ok"

    distinct = set(file_modes_nontrivial)
    if len(distinct) == 1:
        return next(iter(distinct))
    if "output_missing" in distinct and len(distinct) == 2 and "ok" in set(file_modes):
        return "output_missing"
    return "mixed"


# ---------------------------------------------------------------------------
# Confidence
# ---------------------------------------------------------------------------


def confidence_grade(task_result: dict) -> str:
    per_file = task_result.get("per_file") or []
    if not per_file:
        return "low"
    any_byte = any(fs.get("bytes_identical") for fs in per_file)
    any_sidecar = any((fs.get("details") or {}).get("rds_diag") for fs in per_file)
    scores = [fs.get("strategy_score", 0.0) for fs in per_file]
    max_score = max(scores) if scores else 0.0

    if any_byte:
        return "high"
    # High if at least one tabular-aligned ≥0.9 match
    for fs in per_file:
        tab = (fs.get("details") or {}).get("tabular") or {}
        if tab:
            cells_total = tab.get("cells_total", 0) or 0
            cells_matched = tab.get("cells_matched", 0) or 0
            if cells_total and cells_matched / cells_total >= 0.9 and not tab.get("cols_mismatch"):
                return "high"
    if any_sidecar:
        return "low"
    if 0.5 <= max_score <= 0.9:
        return "medium"
    return "low" if max_score < 0.5 else "medium"


# ---------------------------------------------------------------------------
# Actionable fix
# ---------------------------------------------------------------------------


def actionable_fix(
    failure_mode: str,
    task_result: dict,
    traj_info: dict,
) -> str:
    per_file = task_result.get("per_file") or []
    counts = task_result.get("process_counts") or {}

    if failure_mode == "ok":
        return "no action needed"
    if failure_mode == "no_rscript_call":
        return "agent never invoked R; prompt may not have been loaded into context"
    if failure_mode == "rscript_crashed":
        errs = traj_info.get("rscript_errs") or []
        snippet = errs[-1] if errs else "unknown R error"
        return f"R error: {snippet[:100]}"
    if failure_mode == "output_missing":
        missing = [fs.get("filename") for fs in per_file if fs.get("strategy_used") == "missing"]
        return f"rscript exited 0 but expected file(s) absent: {missing}"
    if failure_mode == "schema_drift":
        for fs in per_file:
            tab = (fs.get("details") or {}).get("tabular") or {}
            if tab and tab.get("cols_mismatch"):
                return (
                    f"produced {tab.get('cols_a')} cols vs reference {tab.get('cols_b')} "
                    f"(shared {tab.get('cols_shared')}) on `{fs.get('filename')}`"
                )
        return "column schema differs from reference"
    if failure_mode == "row_drift":
        for fs in per_file:
            tab = (fs.get("details") or {}).get("tabular") or {}
            if tab:
                return (
                    f"cells matched {tab.get('cells_matched')}/{tab.get('cells_total')} "
                    f"({tab.get('cell_match_fraction', 0.0)*100:.0f}%) on `{fs.get('filename')}`"
                )
        return "content drift across rows"
    if failure_mode == "float_drift":
        return "passes at V2 tolerance; regression only under strict byte compare"
    if failure_mode == "rds_semantic_gap":
        for fs in per_file:
            rds = (fs.get("details") or {}).get("rds_diag") or {}
            if rds:
                diag = rds.get("agent") or rds.get("ref") or "unknown"
                return f"sidecar could not reconstruct S4 slot: {diag[:100]}"
        return "rds sidecar returned partial data"
    if failure_mode == "infinite_debug_loop":
        retries = traj_info.get("writes_after_first", 0)
        return (
            f"agent retried {retries} times after first write; consider raising max_steps "
            f"or injecting an explicit recipe"
        )
    if failure_mode == "mixed":
        return "multiple failure modes across expected files — see per-file diff"
    if failure_mode == "missing_reference":
        return "reference ground truth not on disk; evaluator cannot compare"
    return f"unclassified failure (rscript_ok={counts.get('rscript_ok', 0)})"


# ---------------------------------------------------------------------------
# Top-level insight builder
# ---------------------------------------------------------------------------


def build_task_insight(
    task_result: dict,
    *,
    run_dir: Path,
    skill_tokens: list[str],
) -> dict:
    trajectory_path = run_dir / "trajectory.jsonl"
    traj_info = scan_trajectory(trajectory_path, skill_tokens)

    mode = classify_task_failure_mode(task_result, traj_info)
    grade = confidence_grade(task_result)
    fix = actionable_fix(mode, task_result, traj_info)

    per_file_notes = [
        {
            "filename": fs.get("filename"),
            "note": per_file_diff_note(fs),
            "mode": _classify_file_mode(fs),
        }
        for fs in (task_result.get("per_file") or [])
    ]

    return {
        "failure_mode": mode,
        "confidence": grade,
        "actionable_fix": fix,
        "skill_tokens_matched": traj_info["skill_tokens_matched"],
        "skill_tokens_total": len(skill_tokens),
        "skill_tokens_coverage": (
            round(len(traj_info["skill_tokens_matched"]) / len(skill_tokens), 3)
            if skill_tokens else 0.0
        ),
        "steps_total": traj_info["steps_total"],
        "writes_after_first": traj_info["writes_after_first"],
        "rscript_errs": traj_info["rscript_errs"][-3:],
        "per_file_diff": per_file_notes,
    }
