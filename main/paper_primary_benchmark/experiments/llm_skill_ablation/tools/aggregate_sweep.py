#!/usr/bin/env python3
"""Aggregate four-arm sweep results into a per-task matrix + markdown summary.

Reads evaluation JSONs written by
`ldp_r_task_eval/tools/evaluate_real_run.py` (under
`ldp_r_task_eval/runs/_evaluations/sweep_<arm>_<TS>.json`) and emits:

  - `SWEEP_<TS>.json`        : raw matrix + arm/family/difficulty stats.
  - `SWEEP_<TS>_SUMMARY.md`  : prose report with stratified tables.

Token/cost estimates are best-effort: we sum trajectory step counts per arm
and convert with rough per-step averages (GPT-4o @ $2.50/$10 per M
in/out tokens; ~2500 in / 250 out per step for vanilla, ~3200/300 for PAV).
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_ABL = _HERE.parent
_PAPER_PB = _ABL.parent.parent
_LDP = _PAPER_PB / "ldp_r_task_eval"
_EVALS = _LDP / "runs" / "_evaluations"
_RUNS = _LDP / "runs"
_REG = _LDP / "r_tasks" / "registry.real.json"

ARMS = ["vanilla_no_skill", "vanilla_with_skill", "pav_no_skill", "pav_with_skill"]
ARM_CFG = {
    "vanilla_no_skill": {"agent": "SimpleAgent", "skill": False, "max_steps": 32,
                         "config": "config_llm_no_skill.yaml",
                         "tok_in": 2500, "tok_out": 250},
    "vanilla_with_skill": {"agent": "SimpleAgent", "skill": True, "max_steps": 32,
                           "config": "config_llm_with_skill_v2.yaml",
                           "tok_in": 2700, "tok_out": 250},
    "pav_no_skill": {"agent": "PAV", "skill": False, "max_steps": 48,
                     "config": "config_llm_plan_act_verify.yaml",
                     "tok_in": 3200, "tok_out": 300},
    "pav_with_skill": {"agent": "PAV", "skill": True, "max_steps": 48,
                       "config": "config_llm_plan_act_verify_v2.yaml",
                       "tok_in": 3400, "tok_out": 300},
}
DIFFICULTY = {
    "akinyi_deseq2": "medium",
    "riya_limma": "medium",
    "snakepipes_merge_fc": "easy",
    "snakepipes_merge_ct": "easy",
    "chipseq_plot_peak_intersect": "medium",
    "chipseq_plot_macs_qc": "medium",
    "chipseq_plot_homer_annot": "medium",
    "snakepipes_scrna_merge_coutt": "medium",
    "snakepipes_scrna_qc": "hard",
    "epigenbutton_mapping_stats": "medium",
    "epigenbutton_peak_stats": "medium",
    "smartseqtotal_violin": "easy",
}


def _load_eval(batch_id: str) -> dict:
    p = _EVALS / f"{batch_id}.json"
    if not p.is_file():
        raise FileNotFoundError(f"evaluation json missing: {p}")
    return json.loads(p.read_text(encoding="utf-8"))


def _count_steps(batch_id: str) -> dict[str, int]:
    """Return {task_id: step_count} from trajectory.jsonl line counts."""
    root = _RUNS / f"batch_{batch_id}"
    result: dict[str, int] = {}
    if not root.is_dir():
        return result
    for child in sorted(root.iterdir()):
        if not child.is_dir():
            continue
        meta_p = child / "metadata.json"
        tj = child / "trajectory.jsonl"
        if not meta_p.is_file() or not tj.is_file():
            continue
        try:
            meta = json.loads(meta_p.read_text(encoding="utf-8"))
        except Exception:
            continue
        task_id = meta.get("task_id")
        if not task_id:
            continue
        with tj.open(encoding="utf-8") as f:
            n = sum(1 for _ in f)
        result[task_id] = max(0, n - 1)
    return result


def _tally(results: list[dict], key: str) -> dict[str, dict[str, int]]:
    """Group verdict counts by an attribute key ('family' or 'difficulty')."""
    out: dict[str, dict[str, int]] = {}
    for r in results:
        k = r.get(key) or "?"
        bucket = out.setdefault(k, {"pass": 0, "partial": 0, "fail": 0, "error": 0, "n": 0})
        v = r.get("verdict") or "error"
        bucket[v] = bucket.get(v, 0) + 1
        bucket["n"] += 1
    return out


def build_matrix(ts: str, registry: dict) -> dict:
    family_by_task = {t["id"]: t.get("family", "?") for t in registry.get("tasks", [])}
    all_tasks = [t["id"] for t in registry.get("tasks", [])]

    arm_data: dict[str, dict] = {}
    for arm in ARMS:
        bid = f"sweep_{arm}_{ts}"
        ev = _load_eval(bid)
        steps = _count_steps(bid)
        per_task = {}
        for res in ev["results"]:
            tid = res["task_id"]
            per_task[tid] = {
                "verdict": res.get("verdict"),
                "n_expected": res.get("n_expected", 0),
                "n_exists": res.get("n_exists", 0),
                "n_byte_identical": res.get("n_byte_identical", 0),
                "n_table_full_match": res.get("n_table_full_match", 0),
                "family": family_by_task.get(tid, "?"),
                "difficulty": DIFFICULTY.get(tid, "?"),
                "steps": steps.get(tid, 0),
            }
        arm_data[arm] = {
            "batch_run_id": bid,
            "n_tasks": ev["n_tasks"],
            "n_pass": ev["n_pass"],
            "n_partial": ev["n_partial"],
            "n_fail": ev["n_fail"],
            "pass_rate": ev.get("pass_rate"),
            "per_task": per_task,
        }

    matrix = []
    for tid in all_tasks:
        row = {
            "task_id": tid,
            "family": family_by_task.get(tid, "?"),
            "difficulty": DIFFICULTY.get(tid, "?"),
        }
        for arm in ARMS:
            row[arm] = arm_data[arm]["per_task"].get(tid, {}).get("verdict", "error")
        matrix.append(row)

    stratified: dict[str, dict] = {"by_family": {}, "by_difficulty": {}}
    for arm in ARMS:
        arm_results = [
            {"verdict": info["verdict"], "family": info["family"], "difficulty": info["difficulty"]}
            for info in arm_data[arm]["per_task"].values()
        ]
        stratified["by_family"][arm] = _tally(arm_results, "family")
        stratified["by_difficulty"][arm] = _tally(arm_results, "difficulty")

    cost_est: dict[str, dict] = {}
    for arm in ARMS:
        cfg = ARM_CFG[arm]
        steps_total = sum(info["steps"] for info in arm_data[arm]["per_task"].values())
        tok_in = steps_total * cfg["tok_in"]
        tok_out = steps_total * cfg["tok_out"]
        usd = tok_in / 1e6 * 2.50 + tok_out / 1e6 * 10.0
        cost_est[arm] = {
            "steps_total": steps_total,
            "est_tokens_in": tok_in,
            "est_tokens_out": tok_out,
            "est_usd": round(usd, 4),
        }

    return {
        "ts": ts,
        "arms": arm_data,
        "matrix": matrix,
        "stratified": stratified,
        "cost_est": cost_est,
    }


def _md_arm_overview(agg: dict) -> list[str]:
    L = ["## Overall verdict counts per arm\n",
         "| arm | config | agent | skill | max_steps | pass | partial | fail | pass_rate |",
         "|-----|--------|-------|-------|-----------|------|---------|------|-----------|"]
    for arm in ARMS:
        cfg = ARM_CFG[arm]
        a = agg["arms"][arm]
        pr = a.get("pass_rate") or 0.0
        L.append(
            f"| `{arm}` | {cfg['config']} | {cfg['agent']} | {'yes' if cfg['skill'] else 'no'} | "
            f"{cfg['max_steps']} | {a['n_pass']} | {a['n_partial']} | {a['n_fail']} | {pr:.1f}% |"
        )
    L.append("")
    return L


def _md_stratified(agg: dict) -> list[str]:
    L = ["## Stratified results\n"]
    for key, label in (("by_family", "family"), ("by_difficulty", "difficulty")):
        L.append(f"### Pass rate by {label}\n")
        families = sorted({k for arm in ARMS for k in agg["stratified"][key][arm].keys()})
        head = "| arm | " + " | ".join(families) + " |"
        sep = "|-----|" + "|".join(["------"] * len(families)) + "|"
        L.append(head)
        L.append(sep)
        for arm in ARMS:
            cells = []
            for fam in families:
                bucket = agg["stratified"][key][arm].get(fam, {"pass": 0, "n": 0})
                n = bucket.get("n", 0)
                p = bucket.get("pass", 0)
                cells.append(f"{p}/{n}" if n else "–")
            L.append(f"| `{arm}` | " + " | ".join(cells) + " |")
        L.append("")
    return L


def _md_matrix(agg: dict) -> list[str]:
    L = ["## Task-by-task verdict matrix\n",
         "| task | family | difficulty | " + " | ".join(f"`{a}`" for a in ARMS) + " |",
         "|------|--------|-----------|" + "|".join(["---"] * len(ARMS)) + "|"]
    for row in agg["matrix"]:
        cells = [row.get(a, "error") for a in ARMS]
        pretty = [("**pass**" if v == "pass" else v) for v in cells]
        L.append(
            f"| `{row['task_id']}` | {row['family']} | {row['difficulty']} | "
            + " | ".join(pretty) + " |"
        )
    L.append("")
    return L


def _md_cost(agg: dict) -> list[str]:
    L = ["## Token usage + estimated cost (best-effort)\n",
         "Estimate per step: vanilla ~2.5k in / 250 out; PAV ~3.2k in / 300 out (GPT-4o "
         "list: $2.50 / $10.00 per M in/out tokens). Steps counted from `trajectory.jsonl` "
         "line counts.\n",
         "| arm | total steps | est. input tok | est. output tok | est. USD |",
         "|-----|------------:|---------------:|----------------:|---------:|"]
    total_usd = 0.0
    for arm in ARMS:
        c = agg["cost_est"][arm]
        total_usd += c["est_usd"]
        L.append(
            f"| `{arm}` | {c['steps_total']} | {c['est_tokens_in']:,} | "
            f"{c['est_tokens_out']:,} | ${c['est_usd']:.3f} |"
        )
    L.append(f"| **total** | | | | **${total_usd:.3f}** |")
    L.append("")
    return L


def _md_observations(agg: dict) -> list[str]:
    arms = agg["arms"]
    matrix = {r["task_id"]: r for r in agg["matrix"]}
    L = ["## Key observations\n"]

    v_ns = arms["vanilla_no_skill"]["n_pass"]
    v_ws = arms["vanilla_with_skill"]["n_pass"]
    p_ns = arms["pav_no_skill"]["n_pass"]
    p_ws = arms["pav_with_skill"]["n_pass"]
    L.append(
        f"- **Does PAV beat vanilla?** No-skill: PAV {p_ns} vs vanilla {v_ns}. "
        f"With-skill: PAV {p_ws} vs vanilla {v_ws}. "
        f"→ PAV " + ("helps" if (p_ns + p_ws) > (v_ns + v_ws) else "does not help" if (p_ns + p_ws) < (v_ns + v_ws) else "is neutral")
        + " on pass count overall."
    )

    ak = matrix.get("akinyi_deseq2", {})
    L.append(
        f"- **Skill on `akinyi_deseq2` (only task with a paper skill)**: "
        f"vanilla_no_skill={ak.get('vanilla_no_skill')}, "
        f"vanilla_with_skill={ak.get('vanilla_with_skill')}, "
        f"pav_no_skill={ak.get('pav_no_skill')}, "
        f"pav_with_skill={ak.get('pav_with_skill')}."
    )

    llm_fails: list[str] = []
    for tid, row in matrix.items():
        all_llm_nonpass = all(row.get(a) != "pass" for a in ARMS)
        if all_llm_nonpass:
            llm_fails.append(tid)
    L.append(
        f"- **Tasks no LLM arm passes ({len(llm_fails)})**: "
        + (", ".join(f"`{t}`" for t in llm_fails) if llm_fails else "none")
        + ". These define the current hardness ceiling for GPT-4o on this benchmark."
    )

    skill_wins: list[str] = []
    for tid, row in matrix.items():
        if row.get("vanilla_with_skill") == "pass" and row.get("vanilla_no_skill") != "pass":
            skill_wins.append(tid)
        if row.get("pav_with_skill") == "pass" and row.get("pav_no_skill") != "pass":
            if tid not in skill_wins:
                skill_wins.append(tid)
    L.append(
        f"- **Tasks where injecting the skill flipped a failure to a pass**: "
        + (", ".join(f"`{t}`" for t in skill_wins) if skill_wins else "none")
        + "."
    )

    pav_wins: list[str] = []
    for tid, row in matrix.items():
        if row.get("pav_no_skill") == "pass" and row.get("vanilla_no_skill") != "pass":
            pav_wins.append(tid)
    L.append(
        f"- **Tasks where PAV (no skill) flipped a vanilla failure to a pass**: "
        + (", ".join(f"`{t}`" for t in pav_wins) if pav_wins else "none")
        + "."
    )
    L.append("")
    return L


def _md_setup(ts: str) -> list[str]:
    return [
        f"# Four-arm sweep summary — TS `{ts}`\n",
        "## Experiment setup\n",
        "| arm | config | agent | skill manifest | max_steps |",
        "|-----|--------|-------|----------------|-----------|",
        *[f"| `{a}` | `{ARM_CFG[a]['config']}` | {ARM_CFG[a]['agent']} | "
          f"{'yes' if ARM_CFG[a]['skill'] else 'no'} | {ARM_CFG[a]['max_steps']} |" for a in ARMS],
        "",
        f"Registry: `ldp_r_task_eval/r_tasks/registry.real.json` (12 tasks).",
        f"Skill manifest: `experiments/skills/manifest.json` (1 task has a skill: "
        f"`akinyi_deseq2` → Conesa 2016 / `10.1186_s13059-016-0881-8`).",
        f"Evaluator: `ldp_r_task_eval/tools/evaluate_real_run.py` — verdicts are",
        "`pass` (all expected files byte-identical **or** table-full-match), "
        "`partial` (files exist but differ), `fail` (missing files), `error` (run crashed).",
        "",
    ]


def render_markdown(agg: dict) -> str:
    ts = agg["ts"]
    L = []
    L += _md_setup(ts)
    L += _md_arm_overview(agg)
    L += _md_stratified(agg)
    L += _md_matrix(agg)
    L += _md_observations(agg)
    L += _md_cost(agg)
    return "\n".join(L)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--ts", required=True, help="Shared timestamp used for all four sweep batch-run-ids")
    p.add_argument("--out-dir", default=str(_ABL), help="Where to write SWEEP_<ts>.json/.md")
    args = p.parse_args()

    registry = json.loads(_REG.read_text(encoding="utf-8"))
    agg = build_matrix(args.ts, registry)

    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"SWEEP_{args.ts}.json").write_text(json.dumps(agg, indent=2))
    (out_dir / f"SWEEP_{args.ts}_SUMMARY.md").write_text(render_markdown(agg))
    print(f"wrote {out_dir / f'SWEEP_{args.ts}.json'}")
    print(f"wrote {out_dir / f'SWEEP_{args.ts}_SUMMARY.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
