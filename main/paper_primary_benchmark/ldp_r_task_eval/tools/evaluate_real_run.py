#!/usr/bin/env python3
"""Compare an agent's run outputs against per-task ground truth.

For each run directory under `ldp_r_task_eval/runs/batch_<id>/<index>_<task_id>/`,
this tool:
  1. Loads `metadata.json` to find `task_id`.
  2. Looks up the task in the real tasks registry (registry.real.json).
  3. Finds the ground-truth outputs at
     `ldp_r_task_eval/tasks/real_ground_truth/<task_id>/reference_output/*`.
  4. Compares each expected file against the agent's `workspace/output/<file>`.
  5. Scores: exact-match (byte-identical), line-match-count (for text files),
     column-numeric-tolerance (for TSV/CSV files), or byte-size-only for PNG.

Output: a JSON report per batch + a markdown summary.

Usage:
  python3 tools/evaluate_real_run.py --batch-run-id real_no_skill_20260417
  python3 tools/evaluate_real_run.py --all    # evaluate every batch_*
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_LDP = _HERE.parent
_RUNS = _LDP / "runs"
_GT = _LDP / "tasks" / "real_ground_truth"
_REG = _LDP / "r_tasks" / "registry.real.json"


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _try_read_table(path: Path) -> list[list[str]] | None:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return None
    sep = "\t" if "\t" in text.splitlines()[0] else ("," if "," in text.splitlines()[0] else None)
    if sep is None:
        return None
    rows = [row for row in csv.reader(text.splitlines(), delimiter=sep)]
    return rows


def _numeric_tolerance_match(agent_rows: list[list[str]], gt_rows: list[list[str]], rtol: float = 1e-3, atol: float = 1e-5) -> dict:
    """Compare two tables, allowing numeric approximation. Returns breakdown."""
    same_shape = len(agent_rows) == len(gt_rows) and (
        all(len(a) == len(g) for a, g in zip(agent_rows, gt_rows))
    )
    cells_total = 0
    cells_numeric = 0
    cells_numeric_match = 0
    cells_string_match = 0
    cells_string_total = 0
    if not same_shape:
        return {
            "same_shape": False,
            "agent_rows": len(agent_rows),
            "gt_rows": len(gt_rows),
        }
    for ar, gr in zip(agent_rows, gt_rows):
        for a, g in zip(ar, gr):
            cells_total += 1
            try:
                fa = float(a)
                fg = float(g)
                cells_numeric += 1
                if math.isclose(fa, fg, rel_tol=rtol, abs_tol=atol):
                    cells_numeric_match += 1
            except ValueError:
                cells_string_total += 1
                if a == g:
                    cells_string_match += 1
    return {
        "same_shape": True,
        "rows": len(agent_rows),
        "cells_total": cells_total,
        "cells_numeric": cells_numeric,
        "cells_numeric_match": cells_numeric_match,
        "cells_numeric_pct": (cells_numeric_match / cells_numeric * 100.0) if cells_numeric else None,
        "cells_string_total": cells_string_total,
        "cells_string_match": cells_string_match,
        "cells_string_pct": (cells_string_match / cells_string_total * 100.0) if cells_string_total else None,
    }


def _score_file(agent_path: Path, gt_path: Path) -> dict:
    if not agent_path.is_file():
        return {"exists": False, "reason": "missing_in_agent_output"}
    if not gt_path.is_file():
        return {"exists": True, "reason": "missing_ground_truth"}
    score: dict = {"exists": True, "byte_size_agent": agent_path.stat().st_size, "byte_size_gt": gt_path.stat().st_size}
    h_a = _sha256(agent_path)
    h_g = _sha256(gt_path)
    score["sha256_agent"] = h_a
    score["sha256_gt"] = h_g
    score["byte_identical"] = h_a == h_g
    if agent_path.suffix.lower() in {".png", ".pdf", ".jpg", ".jpeg"}:
        return score
    a_rows = _try_read_table(agent_path)
    g_rows = _try_read_table(gt_path)
    if a_rows is not None and g_rows is not None:
        score["table"] = _numeric_tolerance_match(a_rows, g_rows)
    return score


def evaluate_run_dir(run_dir: Path, registry: dict) -> dict:
    meta_path = run_dir / "metadata.json"
    if not meta_path.is_file():
        return {"run_dir": str(run_dir), "error": "no_metadata"}
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    task_id = meta.get("task_id")
    entry = next((t for t in registry.get("tasks", []) if t["id"] == task_id), None)
    if entry is None:
        return {"run_dir": str(run_dir), "task_id": task_id, "error": "task_not_in_registry"}
    expected = entry.get("evaluation", {}).get("expected_files", [])
    gt_dir = _GT / task_id / "reference_output"
    agent_output = (run_dir / "workspace" / "output") if (run_dir / "workspace").is_dir() else Path(meta["work_dir"]) / "output"

    files = {}
    for rel in expected:
        files[rel] = _score_file(agent_output / rel, gt_dir / rel)
    n_expected = len(expected)
    n_exists = sum(1 for v in files.values() if v.get("exists"))
    n_byte_identical = sum(1 for v in files.values() if v.get("byte_identical"))
    n_table_full_match = 0
    for v in files.values():
        tbl = v.get("table") or {}
        num = tbl.get("cells_numeric_match") or 0
        num_t = tbl.get("cells_numeric") or 0
        str_m = tbl.get("cells_string_match") or 0
        str_t = tbl.get("cells_string_total") or 0
        if tbl.get("same_shape") and num == num_t and str_m == str_t:
            n_table_full_match += 1
    verdict = "pass" if n_byte_identical == n_expected or n_table_full_match == n_expected else (
        "partial" if n_exists else "fail"
    )
    return {
        "run_dir": str(run_dir),
        "task_id": task_id,
        "batch_run_id": meta.get("batch_run_id"),
        "model": (meta.get("agent") or {}).get("llm_model"),
        "smoke": meta.get("smoke"),
        "n_expected": n_expected,
        "n_exists": n_exists,
        "n_byte_identical": n_byte_identical,
        "n_table_full_match": n_table_full_match,
        "verdict": verdict,
        "files": files,
    }


def evaluate_batch(batch_run_id: str, registry: dict) -> dict:
    batch_root = _RUNS / f"batch_{batch_run_id}"
    if not batch_root.is_dir():
        raise FileNotFoundError(f"batch directory not found: {batch_root}")
    per_task = []
    for child in sorted(batch_root.iterdir()):
        if child.is_dir():
            per_task.append(evaluate_run_dir(child, registry))
    n = len(per_task)
    n_pass = sum(1 for r in per_task if r.get("verdict") == "pass")
    n_partial = sum(1 for r in per_task if r.get("verdict") == "partial")
    n_fail = sum(1 for r in per_task if r.get("verdict") == "fail")
    return {
        "batch_run_id": batch_run_id,
        "batch_root": str(batch_root),
        "n_tasks": n,
        "n_pass": n_pass,
        "n_partial": n_partial,
        "n_fail": n_fail,
        "pass_rate": (n_pass / n * 100.0) if n else None,
        "results": per_task,
    }


def _render_markdown(summary: dict) -> str:
    lines = []
    lines.append(f"# Evaluation summary for batch `{summary['batch_run_id']}`\n")
    lines.append(
        f"**Tasks:** {summary['n_tasks']} | pass: {summary['n_pass']} | partial: {summary['n_partial']} | fail: {summary['n_fail']} | pass_rate: {summary['pass_rate']:.1f}%\n"
        if summary.get("pass_rate") is not None
        else f"**Tasks:** {summary['n_tasks']} (no results)\n"
    )
    lines.append("| task | verdict | byte-identical | table-full-match | expected | exists |")
    lines.append("|------|---------|----------------|------------------|----------|--------|")
    for r in summary["results"]:
        lines.append(
            f"| `{r.get('task_id')}` | **{r.get('verdict')}** | {r.get('n_byte_identical', 0)} | {r.get('n_table_full_match', 0)} | {r.get('n_expected', 0)} | {r.get('n_exists', 0)} |"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--batch-run-id", action="append", help="Specific batch id (repeatable)")
    p.add_argument("--all", action="store_true", help="Evaluate all batch_* directories")
    p.add_argument("--registry", default=str(_REG))
    args = p.parse_args()

    registry = json.loads(Path(args.registry).read_text(encoding="utf-8"))
    targets: list[str] = []
    if args.all:
        for d in _RUNS.glob("batch_*"):
            if d.is_dir():
                targets.append(d.name.removeprefix("batch_"))
    if args.batch_run_id:
        targets.extend([b for b in args.batch_run_id if b not in targets])
    if not targets:
        p.error("pass --batch-run-id or --all")

    out_dir = _LDP / "runs" / "_evaluations"
    out_dir.mkdir(parents=True, exist_ok=True)
    for bid in targets:
        try:
            summary = evaluate_batch(bid, registry)
        except FileNotFoundError as e:
            print(f"skip {bid}: {e}", file=sys.stderr)
            continue
        (out_dir / f"{bid}.json").write_text(json.dumps(summary, indent=2))
        (out_dir / f"{bid}.md").write_text(_render_markdown(summary))
        print(_render_markdown(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
