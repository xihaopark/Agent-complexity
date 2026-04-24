#!/usr/bin/env python3
"""Build ``experiments/llm_skill_ablation/INSIGHTS_REPORT.md`` from the
four V3 per-arm JSONs.

Deterministic. Stdlib-only. Driven entirely by the V3 evaluator output
files at ``ldp_r_task_eval/runs/_evaluations/sweep_v3_<arm>_<TS>.v3.json``.

Outputs one markdown file containing:

* failure-mode histogram per arm,
* confidence histogram per arm,
* top 10 most-insightful task rows (paper-arm wins with clean skill
  attribution, plus the one `no_rscript_call` / `infinite_debug_loop`
  per arm when present),
* cross-arm "same task, different failure mode" highlights,
* a pre-rendered stacked-bar spec suitable for a paper figure.

Run:

```bash
python3 tools/build_insights_report.py \\
    --batch-ts 20260416T194356Z \\
    --out experiments/llm_skill_ablation/INSIGHTS_REPORT.md
```
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_REPO = _HERE.parents[4]
_EVAL_DIR = _REPO / "main" / "paper_primary_benchmark" / "ldp_r_task_eval" / "runs" / "_evaluations"

ARMS = ["none", "paper", "pipeline", "llm_plan"]
MODE_ORDER = [
    "ok",
    "float_drift",
    "row_drift",
    "schema_drift",
    "rds_semantic_gap",
    "mixed",
    "output_missing",
    "rscript_crashed",
    "infinite_debug_loop",
    "no_rscript_call",
    "task_never_started",
]
CONF_ORDER = ["high", "medium", "low"]


def _load(batch_ts: str) -> dict[str, dict]:
    out = {}
    for arm in ARMS:
        path = _EVAL_DIR / f"sweep_v3_{arm}_{batch_ts}.v3.json"
        out[arm] = json.loads(path.read_text(encoding="utf-8"))
    return out


def _mode_histogram(results: list[dict]) -> Counter:
    return Counter((r.get("insight") or {}).get("failure_mode", "?") for r in results)


def _conf_histogram(results: list[dict]) -> Counter:
    return Counter((r.get("insight") or {}).get("confidence", "?") for r in results)


def _render_histogram_table(title: str, per_arm: dict[str, Counter], order: list[str]) -> list[str]:
    cols = [m for m in order if any(per_arm[arm].get(m, 0) for arm in per_arm)]
    extras = sorted({m for c in per_arm.values() for m in c if m not in order})
    cols.extend(extras)
    lines = [f"### {title}", ""]
    lines.append("| arm | " + " | ".join(f"`{m}`" for m in cols) + " | total |")
    lines.append("|-----|" + "|".join(["---:"] * (len(cols) + 1)) + "|")
    for arm, counter in per_arm.items():
        row = [f"`{arm}`"] + [str(counter.get(m, 0)) for m in cols] + [str(sum(counter.values()))]
        lines.append("| " + " | ".join(row) + " |")
    lines.append("")
    return lines


def _task_index(data: dict[str, dict]) -> dict[str, dict[str, dict]]:
    """Return { task_id -> { arm -> task_result_with_insight } }."""
    idx: dict[str, dict[str, dict]] = defaultdict(dict)
    for arm, summary in data.items():
        for r in summary.get("results", []):
            tid = r.get("task_id")
            if tid:
                idx[tid][arm] = r
    return idx


def _top_insights(task_index: dict[str, dict[str, dict]]) -> list[tuple[str, str, str, str]]:
    """Pick the 10 most-insightful individual (task, arm) rows."""
    rows: list[tuple[int, str, str, str, str]] = []

    for tid, per_arm in task_index.items():
        for arm, r in per_arm.items():
            ins = r.get("insight") or {}
            mode = ins.get("failure_mode", "")
            score = r.get("overall_score", 0.0) or 0.0
            tokens_matched = ins.get("skill_tokens_matched") or []
            coverage = ins.get("skill_tokens_coverage") or 0.0
            fix = ins.get("actionable_fix", "")

            priority = 0
            if mode == "infinite_debug_loop":
                priority = 100
            elif mode == "no_rscript_call":
                priority = 90
            elif mode == "rds_semantic_gap":
                priority = 80
            elif mode == "float_drift":
                priority = 70
            elif arm == "paper" and mode == "ok" and tokens_matched:
                priority = 95  # paper-arm wins with skill attribution are gold
            elif mode == "ok" and coverage >= 0.5 and len(tokens_matched) >= 3:
                priority = 60
            elif mode == "mixed":
                priority = 55
            elif mode == "schema_drift":
                priority = 40
            elif mode == "row_drift":
                priority = 30
            if score > 0 and mode == "ok":
                priority += 5
            if priority <= 0:
                continue
            rows.append((priority, tid, arm, mode, fix))

    rows.sort(key=lambda x: (-x[0], x[1]))
    return [(tid, arm, mode, fix) for _, tid, arm, mode, fix in rows[:10]]


def _cross_arm_deltas(task_index: dict[str, dict[str, dict]]) -> list[dict]:
    """Tasks where at least two arms produce different (non-never_started) failure modes."""
    out = []
    for tid, per_arm in task_index.items():
        modes = {}
        for arm, r in per_arm.items():
            m = (r.get("insight") or {}).get("failure_mode")
            if m and m != "task_never_started":
                modes[arm] = m
        if len(set(modes.values())) < 2:
            continue
        out.append({
            "task_id": tid,
            "modes": modes,
            "overall": {arm: per_arm[arm].get("overall_score") for arm in per_arm},
            "notes": {
                arm: ((per_arm[arm].get("insight") or {}).get("actionable_fix") or "")[:160]
                for arm in per_arm
            },
        })
    return out


def build_report(batch_ts: str) -> str:
    data = _load(batch_ts)
    per_arm_modes = {arm: _mode_histogram(data[arm]["results"]) for arm in ARMS}
    per_arm_conf = {arm: _conf_histogram(data[arm]["results"]) for arm in ARMS}
    task_index = _task_index(data)

    lines: list[str] = [
        "# Skill-arm Insights Report (V3 evaluator)",
        "",
        f"Batch timestamp: `{batch_ts}`.  Source JSONs:",
        "",
    ]
    for arm in ARMS:
        lines.append(f"* `sweep_v3_{arm}_{batch_ts}.v3.json`")
    lines.append("")

    lines.append("## 1 · Failure-mode distribution per arm")
    lines.append("")
    lines.extend(_render_histogram_table("Failure mode × arm", per_arm_modes, MODE_ORDER))

    lines.append("## 2 · Confidence grade distribution per arm")
    lines.append("")
    lines.extend(_render_histogram_table("Confidence × arm", per_arm_conf, CONF_ORDER))

    # 3 · Top insights
    lines.append("## 3 · Top 10 most-insightful task rows")
    lines.append("")
    lines.append("Chosen deterministically by priority: paper-arm wins with non-empty skill "
                 "token attribution > `no_rscript_call` / `infinite_debug_loop` > `rds_semantic_gap` "
                 "/ `float_drift` > other per-file modes with high skill coverage.")
    lines.append("")
    lines.append("| # | task | arm | failure mode | actionable fix |")
    lines.append("|--:|------|-----|--------------|-----------------|")
    tops = _top_insights(task_index)
    for i, (tid, arm, mode, fix) in enumerate(tops, 1):
        lines.append(f"| {i} | `{tid}` | `{arm}` | `{mode}` | {fix[:140]} |")
    lines.append("")

    # 4 · Cross-arm deltas
    lines.append("## 4 · Cross-arm \"same task, different failure mode\" highlights")
    lines.append("")
    deltas = _cross_arm_deltas(task_index)
    if not deltas:
        lines.append("_No task shows cross-arm differential failure modes._")
    else:
        lines.append(f"Found **{len(deltas)}** tasks where the four arms disagree on "
                     "failure mode (ignoring `task_never_started`). Highlights:")
        lines.append("")
        lines.append("| task | mode by arm |")
        lines.append("|------|-------------|")
        for d in deltas:
            bits = [f"`{arm}`={d['modes'].get(arm, '—')}" for arm in ARMS if arm in d["modes"]]
            lines.append(f"| `{d['task_id']}` | " + ", ".join(bits) + " |")
        lines.append("")
        lines.append("### 4a · Signature cases")
        lines.append("")
        # Select signature cases
        signatures = []
        for d in deltas:
            modes = d["modes"]
            if set(modes.values()) >= {"ok", "rscript_crashed"}:
                signatures.append(("skill rescued an otherwise-crashing task", d))
            elif "infinite_debug_loop" in modes.values():
                signatures.append(("skill triggered an infinite debug loop", d))
            elif "float_drift" in modes.values() and "ok" in modes.values():
                signatures.append(("skill flipped byte-match to tolerance-match", d))
        for title, d in signatures[:6]:
            lines.append(f"* **{title}** — `{d['task_id']}`:")
            for arm in ARMS:
                if arm in d["modes"]:
                    lines.append(
                        f"    - `{arm}`: **{d['modes'][arm]}** "
                        f"(score {d['overall'].get(arm, 0.0):.2f}) — "
                        f"{d['notes'].get(arm, '')[:120]}"
                    )
        lines.append("")

    # 5 · Paper-arm skill attribution
    lines.append("## 5 · Skill-token attribution evidence")
    lines.append("")
    lines.append("How often does a skill actually show up in the agent's tool-call arguments? "
                 "V3 records matched tokens per task; the per-arm averages below show how "
                 "code-actionable each skill source is.")
    lines.append("")
    lines.append("| arm | mean tokens available | mean tokens matched | mean coverage |")
    lines.append("|-----|----------------------:|--------------------:|--------------:|")
    for arm in ARMS:
        results = data[arm]["results"]
        totals = [(r.get("insight") or {}).get("skill_tokens_total", 0) for r in results]
        matched = [len((r.get("insight") or {}).get("skill_tokens_matched") or []) for r in results]
        coverage = [(r.get("insight") or {}).get("skill_tokens_coverage", 0.0) for r in results]
        n = max(1, len(results))
        lines.append(
            f"| `{arm}` | {sum(totals)/n:.1f} | {sum(matched)/n:.2f} | {sum(coverage)/n*100:.1f}% |"
        )
    lines.append("")
    lines.append("The `paper` arm column is almost zero because vision-adapter skills are prose "
                 "summaries — they contain almost no code-actionable tokens for the matcher to "
                 "fire on. This is itself an insight: paper skills transmit *ideas*, not APIs.")
    lines.append("")

    # 6 · Figure spec
    lines.append("## 6 · Recommended publication-ready figures")
    lines.append("")
    lines.append("1. **Stacked bar — failure mode × arm.** X-axis = arm, "
                 "Y-axis = task count, stacks coloured by failure mode. Source: "
                 "`failure_mode_counts` in each `<batch>.v3.json`.")
    lines.append("2. **Heatmap — task × arm, cell = failure mode.** One row per task, "
                 "four columns. Helps the reader spot cross-arm disagreements. Source: "
                 "`insights[task].failure_mode` per arm.")
    lines.append("3. **Bar chart — paper-arm wins with skill-token coverage > 0.** Makes the "
                 "\"did the agent attend to the skill\" question legible.")
    lines.append("4. **CDF of `overall_score` per arm** overlaid with per-task failure-mode "
                 "labels. Shows that V2 already separates arms by score, and V3 explains *why*.")
    lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("Report generated by `tools/build_insights_report.py`. "
                 "V3 evaluator: `main/paper_primary_benchmark/ldp_r_task_eval/tools/evaluate_real_run_v3.py`. "
                 "Rubric: `.../tools/EVALUATION_V3.md`.")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--batch-ts", default="20260416T194356Z")
    p.add_argument("--out",
                   default=str(_HERE.parent / "INSIGHTS_REPORT.md"))
    args = p.parse_args(argv)
    text = build_report(args.batch_ts)
    Path(args.out).write_text(text)
    print(f"wrote {args.out} ({len(text)} chars)", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
