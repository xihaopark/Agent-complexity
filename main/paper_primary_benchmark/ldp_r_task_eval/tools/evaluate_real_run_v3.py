#!/usr/bin/env python3
"""V3 insight-oriented evaluator for ldp R-task runs.

V3 extends V2 rather than replacing it: it re-uses ``evaluate_real_run_v2``
to produce per-task scores and strategies, then adds a deterministic
"insight" layer per task that explains **why** the score is what it is.

For each task V3 emits:

* ``failure_mode`` (enum; see ``EVALUATION_V3.md`` for the catalog)
* ``confidence`` (high / medium / low)
* ``actionable_fix`` (one-line suggestion keyed on failure mode)
* ``skill_tokens_matched`` (tokens from the arm's skill manifest that the
  agent actually surfaced in a tool-call argument — a "did the agent read
  the skill?" signal)
* per-file diff notes (≤ 120 chars each)

V3 does not recompute V2 scores when ``--insight-only`` is passed and a
cached ``<batch>.v2.json`` is available; it loads that JSON and just adds
the insight block.  This keeps large sweeps cheap to re-analyse.

No LLM calls.  No additional third-party dependencies beyond what V2
already requires (stdlib + pandas/numpy/pyyaml via V2).
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

import evaluate_real_run_v2 as _v2  # noqa: E402
from evaluators.insight import build_task_insight  # noqa: E402

EVALUATOR_VERSION = "v3"
_LDP = _HERE.parent
_RUNS = _LDP / "runs"
_DEFAULT_EVAL_DIR = _LDP / "runs" / "_evaluations"
_DEFAULT_SKILL_TOKENS = _HERE / "evaluators" / "skill_tokens_v3.json"
_DEFAULT_REG = _LDP / "r_tasks" / "registry.real.json"
_DEFAULT_RDS_HELPER = _HERE / "evaluators" / "rds_sidecar.R"


def _arm_from_batch_id(batch_run_id: str) -> str | None:
    """``sweep_v3_paper_20260416T194356Z`` → ``paper``.

    Recognised arms: paper, none, pipeline, llm_plan.
    """
    b = batch_run_id or ""
    for arm in ("llm_plan", "pipeline", "paper", "none"):
        if f"_{arm}_" in b or b.endswith(f"_{arm}"):
            return arm
    return None


def _arm_for_task(task_meta: dict, batch_run_id: str) -> str:
    """Prefer the arm recorded in metadata; fall back to batch-id sniff."""
    skill = task_meta.get("skill") or {}
    arm = skill.get("arm")
    if arm:
        return arm
    return _arm_from_batch_id(batch_run_id) or "none"


def _load_v2_summary(v2_json_path: Path) -> dict:
    return json.loads(v2_json_path.read_text(encoding="utf-8"))


def _skill_tokens_for(task_id: str, arm: str, tokens_map: dict) -> list[str]:
    entry = tokens_map.get(task_id) or {}
    return entry.get(arm) or []


def annotate_with_insights(
    summary: dict,
    tokens_map: dict,
) -> dict:
    """Augment a V2 batch summary in-place with insight blocks and return it."""
    insights: dict[str, dict] = {}
    mode_counts: dict[str, int] = {}
    conf_counts: dict[str, int] = {"high": 0, "medium": 0, "low": 0}

    batch_arm = _arm_from_batch_id(summary.get("batch_run_id", "")) or "none"

    for r in summary.get("results", []):
        task_id = r.get("task_id")
        run_dir = Path(r.get("run_dir") or "")
        # Recover task_id from the "NNN_<task_id>" directory name when V2 found no metadata.
        if not task_id and run_dir.name:
            name = run_dir.name
            if "_" in name and name.split("_", 1)[0].isdigit():
                task_id = name.split("_", 1)[1]
                r["task_id"] = task_id
                r.setdefault("task_id_inferred", True)

        skill_info = r.get("skill") or {}
        arm = skill_info.get("arm") or batch_arm
        skill_tokens = _skill_tokens_for(task_id or "", arm, tokens_map)

        insight = build_task_insight(r, run_dir=run_dir, skill_tokens=skill_tokens)
        insight["arm"] = arm
        if r.get("error") == "no_metadata":
            insight["failure_mode"] = "task_never_started"
            insight["actionable_fix"] = (
                "task never started (no metadata.json; batch runner skipped this row)"
            )
            insight["confidence"] = "high"
        r["insight"] = insight
        if task_id:
            insights[task_id] = insight
        mode = insight["failure_mode"]
        mode_counts[mode] = mode_counts.get(mode, 0) + 1
        conf_counts[insight["confidence"]] = conf_counts.get(insight["confidence"], 0) + 1

    summary["evaluator_version"] = EVALUATOR_VERSION
    summary["insights"] = insights
    summary["failure_mode_counts"] = dict(sorted(mode_counts.items()))
    summary["confidence_counts"] = conf_counts
    summary["ts_v3"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return summary


# ---------------------------------------------------------------------------
# Markdown rendering
# ---------------------------------------------------------------------------


def _render_markdown(summary: dict) -> str:
    lines = [
        f"# Evaluation V3 · batch `{summary['batch_run_id']}`",
        "",
        f"evaluator_version: `{summary.get('evaluator_version')}` · "
        f"ts: `{summary.get('ts_v3', summary.get('ts'))}` · "
        f"n_tasks: {summary.get('n_tasks')} · "
        f"rtol={summary.get('rtol')} atol={summary.get('atol')}",
        "",
        f"**Mean overall score:** {summary.get('mean_score', 0.0):.3f}",
        "",
        "**Verdict counts (V2):** "
        + ", ".join(f"{k}={v}" for k, v in summary.get("verdict_counts", {}).items()),
        "",
        "**Failure-mode distribution (V3):** "
        + ", ".join(f"{k}={v}" for k, v in summary.get("failure_mode_counts", {}).items()),
        "",
        "**Confidence distribution (V3):** "
        + ", ".join(f"{k}={v}" for k, v in summary.get("confidence_counts", {}).items()),
        "",
        "| task | verdict | overall | failure_mode | confidence | insight |",
        "|------|---------|---------|--------------|------------|---------|",
    ]
    for r in summary.get("results", []):
        ins = r.get("insight") or {}
        note_bits = []
        for pf in ins.get("per_file_diff", []):
            note_bits.append(f"`{pf['filename']}`: {pf['note']}")
        joined = " ; ".join(note_bits)[:300]
        lines.append(
            f"| `{r.get('task_id')}` | {r.get('verdict')} | {r.get('overall_score', 0.0):.3f} | "
            f"**{ins.get('failure_mode')}** | {ins.get('confidence')} | {joined} |"
        )
    lines.append("")
    lines.append("## Why (actionable fix per task)")
    lines.append("")
    for r in summary.get("results", []):
        ins = r.get("insight") or {}
        toks = ins.get("skill_tokens_matched") or []
        tok_line = (
            f"skill tokens matched: {len(toks)}/{ins.get('skill_tokens_total', 0)}"
            + (f" ({', '.join(toks[:6])}{'...' if len(toks) > 6 else ''})" if toks else "")
        )
        lines.append(f"### `{r.get('task_id')}` — {ins.get('failure_mode')} ({ins.get('confidence')})")
        lines.append("")
        lines.append(f"- fix: {ins.get('actionable_fix')}")
        lines.append(f"- {tok_line}")
        for pf in ins.get("per_file_diff", []):
            lines.append(f"- `{pf['filename']}` [{pf.get('mode')}]: {pf['note']}")
        errs = ins.get("rscript_errs") or []
        if errs:
            lines.append(f"- last R error: `{errs[-1]}`")
        lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Insight-oriented evaluator for ldp R-task runs (V3).",
    )
    p.add_argument("--batch-run-id", action="append", help="batch id (repeatable)")
    p.add_argument("--all", action="store_true", help="evaluate every runs/batch_*")
    p.add_argument("--registry", default=str(_DEFAULT_REG))
    p.add_argument("--output", default=None, help="directory for json/md outputs")
    p.add_argument("--skill-tokens-json", default=str(_DEFAULT_SKILL_TOKENS))
    p.add_argument("--insight-only", action="store_true",
                   help="skip V2 recomputation; load cached <batch>.v2.json and only add insights")
    p.add_argument("--rds-helper", default=str(_DEFAULT_RDS_HELPER))
    p.add_argument("--rtol", type=float, default=1e-3)
    p.add_argument("--atol", type=float, default=1e-5)
    p.add_argument("--legacy", action="store_true")
    p.add_argument("--quiet", action="store_true")
    args = p.parse_args(argv)

    out_dir = Path(args.output) if args.output else _DEFAULT_EVAL_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    tokens_path = Path(args.skill_tokens_json)
    if tokens_path.is_file():
        tokens_map = json.loads(tokens_path.read_text(encoding="utf-8"))
    else:
        tokens_map = {}
        if not args.quiet:
            print(f"warn: no skill-tokens JSON at {tokens_path}", file=sys.stderr)

    targets: list[str] = []
    if args.all:
        for d in sorted(_RUNS.glob("batch_*")):
            if d.is_dir():
                targets.append(d.name.removeprefix("batch_"))
    if args.batch_run_id:
        for b in args.batch_run_id:
            if b not in targets:
                targets.append(b)
    if not targets:
        p.error("pass --batch-run-id or --all")

    registry = None
    if not args.insight_only:
        registry = json.loads(Path(args.registry).read_text(encoding="utf-8"))
    scratch_root = out_dir / "_rds_scratch"
    scratch_root.mkdir(parents=True, exist_ok=True)

    for bid in targets:
        t0 = time.time()
        v2_cache_path = out_dir / f"{bid}.v2.json"
        summary: dict | None = None
        if args.insight_only:
            if not v2_cache_path.is_file():
                print(f"skip {bid}: v2 cache missing ({v2_cache_path})", file=sys.stderr)
                continue
            summary = _load_v2_summary(v2_cache_path)
        else:
            try:
                summary = _v2.evaluate_batch(
                    bid,
                    registry,
                    rds_helper=Path(args.rds_helper),
                    rtol=args.rtol,
                    atol=args.atol,
                    legacy=args.legacy,
                    scratch_root=scratch_root,
                )
            except FileNotFoundError as e:
                print(f"skip {bid}: {e}", file=sys.stderr)
                continue
            v2_cache_path.write_text(json.dumps(summary, indent=2, default=str))
            (out_dir / f"{bid}.v2.md").write_text(_v2._render_markdown(summary))

        annotate_with_insights(summary, tokens_map)

        (out_dir / f"{bid}.v3.json").write_text(json.dumps(summary, indent=2, default=str))
        (out_dir / f"{bid}.v3.md").write_text(_render_markdown(summary))

        if not args.quiet:
            print(_render_markdown(summary))
            print(f"# {bid}: {time.time() - t0:.1f}s", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
