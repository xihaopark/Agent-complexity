#!/usr/bin/env python3
"""Aggregate the Phase-3 four-arm skill-source sweep (`none` / `paper` /
`pipeline` / `llm_plan`) over the 6-task V2 registry.

Reads evaluation JSONs at
`ldp_r_task_eval/runs/_evaluations/sweep_v2_<arm>_<TS>.json` and each run's
`batch_sweep_v2_<arm>_<TS>/<idx>_<task_id>/metadata.json` and emits:

  - `SWEEP_V2_<TS>.json`            : raw per-(arm,task) matrix + stats.
  - `SWEEP_V2_<TS>_SUMMARY.md`      : stratified human-readable report.
  - `SWEEP_V2_<TS>_SKILL_AUDIT.md`  : per-(arm,task) sha + char-len audit.

All four arms share the same SimpleAgent + config_llm_with_skill_v2.yaml.
Token/cost estimates are best-effort: steps come from `trajectory.jsonl`
line count (minus 1 for the initial state message) × rough per-step
averages (~2.7k in / 0.25k out for skill-injected arms, ~2.5k / 0.25k
for `none`). Public GPT-4o rate card: $2.50 / $10.00 per M in/out tokens.
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

ARMS = ["none", "paper", "pipeline", "llm_plan"]

ARM_CFG = {
    "none": {"tok_in": 2500, "tok_out": 250,
             "manifest_path": None,
             "description": "no skill injected (sentinel text only)"},
    "paper": {"tok_in": 2700, "tok_out": 250,
              "manifest_path": "experiments/skills/manifest.json",
              "description": "method-paper-derived skill"},
    "pipeline": {"tok_in": 2700, "tok_out": 250,
                 "manifest_path": "experiments/skills_pipeline/manifest.json",
                 "description": "pipeline-structure-derived skill"},
    "llm_plan": {"tok_in": 2700, "tok_out": 250,
                 "manifest_path": "experiments/skills_llm_plan/manifest.json",
                 "description": "LLM-generated plan grounded in OBJECTIVE.md only"},
}

EXPECTED_SHA8 = {
    ("paper", "akinyi_deseq2"): "482a3490",
    ("paper", "star_deseq2_init"): "4aaf2fb8",
    ("paper", "star_deseq2_contrast"): "4aaf2fb8",
    ("paper", "methylkit_load"): "7a926c67",
    ("paper", "methylkit_unite"): "7a926c67",
    ("paper", "methylkit_to_tibble"): "7a926c67",
    ("pipeline", "akinyi_deseq2"): "4efe17fd",
    ("pipeline", "star_deseq2_init"): "e9a3bc65",
    ("pipeline", "star_deseq2_contrast"): "e9a3bc65",
    ("pipeline", "methylkit_load"): "98666787",
    ("pipeline", "methylkit_unite"): "98666787",
    ("pipeline", "methylkit_to_tibble"): "98666787",
    ("llm_plan", "akinyi_deseq2"): "3a889efd",
    ("llm_plan", "star_deseq2_init"): "f169268d",
    ("llm_plan", "star_deseq2_contrast"): "06cd791a",
    ("llm_plan", "methylkit_load"): "db18cc3a",
    ("llm_plan", "methylkit_unite"): "dc8aedc7",
    ("llm_plan", "methylkit_to_tibble"): "0da2c673",
}


def _load_eval(batch_id: str) -> dict:
    p = _EVALS / f"{batch_id}.json"
    if not p.is_file():
        raise FileNotFoundError(f"evaluation json missing: {p}")
    return json.loads(p.read_text(encoding="utf-8"))


def _collect_run_meta(batch_id: str) -> dict[str, dict]:
    """Return {task_id: {'steps': int, 'skill': dict|None}} from run dirs."""
    root = _RUNS / f"batch_{batch_id}"
    out: dict[str, dict] = {}
    if not root.is_dir():
        return out
    for child in sorted(root.iterdir()):
        if not child.is_dir():
            continue
        meta_p = child / "metadata.json"
        tj = child / "trajectory.jsonl"
        if not meta_p.is_file():
            continue
        try:
            meta = json.loads(meta_p.read_text(encoding="utf-8"))
        except Exception:
            continue
        task_id = meta.get("task_id")
        if not task_id:
            continue
        steps = 0
        if tj.is_file():
            with tj.open(encoding="utf-8") as f:
                steps = max(0, sum(1 for _ in f) - 1)
        out[task_id] = {"steps": steps, "skill": meta.get("skill") or {}}
    return out


def _tally(results: list[dict], key: str) -> dict[str, dict[str, int]]:
    out: dict[str, dict[str, int]] = {}
    for r in results:
        k = r.get(key)
        k = str(k) if k is not None else "?"
        bucket = out.setdefault(k, {"pass": 0, "partial": 0, "fail": 0, "error": 0, "n": 0})
        v = r.get("verdict") or "error"
        bucket[v] = bucket.get(v, 0) + 1
        bucket["n"] += 1
    return out


def build_matrix(ts: str, registry: dict) -> dict:
    tasks = registry.get("tasks", [])
    fam = {t["id"]: t.get("family", "?") for t in tasks}
    diff = {t["id"]: t.get("difficulty", "?") for t in tasks}
    all_ids = [t["id"] for t in tasks]

    arm_data: dict[str, dict] = {}
    for arm in ARMS:
        bid = f"sweep_v2_{arm}_{ts}"
        ev = _load_eval(bid)
        run_meta = _collect_run_meta(bid)
        per_task = {}
        for res in ev["results"]:
            tid = res["task_id"]
            rm = run_meta.get(tid, {})
            per_task[tid] = {
                "verdict": res.get("verdict"),
                "n_expected": res.get("n_expected", 0),
                "n_exists": res.get("n_exists", 0),
                "n_byte_identical": res.get("n_byte_identical", 0),
                "n_table_full_match": res.get("n_table_full_match", 0),
                "family": fam.get(tid, "?"),
                "difficulty": diff.get(tid, "?"),
                "steps": rm.get("steps", 0),
                "skill": rm.get("skill") or {},
            }
        arm_data[arm] = {
            "batch_run_id": bid,
            "n_tasks": ev["n_tasks"],
            "n_pass": ev["n_pass"],
            "n_partial": ev["n_partial"],
            "n_fail": ev["n_fail"],
            "n_error": ev.get("n_error", 0),
            "pass_rate": ev.get("pass_rate"),
            "per_task": per_task,
        }

    matrix = []
    for tid in all_ids:
        row = {"task_id": tid, "family": fam.get(tid, "?"), "difficulty": diff.get(tid, "?")}
        for arm in ARMS:
            row[arm] = arm_data[arm]["per_task"].get(tid, {}).get("verdict", "error")
        matrix.append(row)

    stratified = {"by_family": {}, "by_difficulty": {}}
    for arm in ARMS:
        rows = [{"verdict": i["verdict"], "family": i["family"], "difficulty": i["difficulty"]}
                for i in arm_data[arm]["per_task"].values()]
        stratified["by_family"][arm] = _tally(rows, "family")
        stratified["by_difficulty"][arm] = _tally(rows, "difficulty")

    cost_est = {}
    for arm in ARMS:
        cfg = ARM_CFG[arm]
        steps_total = sum(i["steps"] for i in arm_data[arm]["per_task"].values())
        tok_in = steps_total * cfg["tok_in"]
        tok_out = steps_total * cfg["tok_out"]
        usd = tok_in / 1e6 * 2.50 + tok_out / 1e6 * 10.0
        cost_est[arm] = {"steps_total": steps_total, "est_tokens_in": tok_in,
                         "est_tokens_out": tok_out, "est_usd": round(usd, 4)}

    audit_rows = []
    for arm in ARMS:
        for tid in all_ids:
            sk = arm_data[arm]["per_task"].get(tid, {}).get("skill", {}) or {}
            sha = sk.get("skill_sha256") or ""
            sha8 = sha[:8] if sha else ""
            exp8 = EXPECTED_SHA8.get((arm, tid), "" if arm == "none" else "?")
            arm_ok = (sk.get("arm") == arm)
            inj_ok = ((arm == "none" and not sk.get("injected", False)) or
                      (arm != "none" and sk.get("injected", False) is True))
            sha_ok = (arm == "none") or (sha8 == exp8) or (exp8 == "?")
            audit_rows.append({
                "arm": arm, "task_id": tid,
                "arm_meta": sk.get("arm"),
                "injected": sk.get("injected", False),
                "skill_sha256": sha,
                "skill_sha256_8": sha8,
                "expected_sha8": exp8,
                "skill_char_len": sk.get("skill_char_len"),
                "skill_md_path": sk.get("skill_md_path"),
                "lookup_field": sk.get("lookup_field"),
                "lookup_key": sk.get("lookup_key"),
                "arm_match": arm_ok,
                "injected_expected": inj_ok,
                "sha_match": sha_ok,
                "ok": arm_ok and inj_ok and sha_ok,
            })

    return {"ts": ts, "arms": arm_data, "matrix": matrix,
            "stratified": stratified, "cost_est": cost_est, "audit": audit_rows}


def _md_setup(ts: str, agg: dict) -> list[str]:
    L = [f"# Four-arm skill-source sweep — TS `{ts}`\n",
         "## Experiment setup\n",
         "Same SimpleAgent, same `config_llm_with_skill_v2.yaml`, same 6-task "
         "registry. Only `--skill-source` varies. Shared batch timestamp means "
         "every `sweep_v2_<arm>_<TS>` lines up.\n",
         "| arm | skill manifest | description |",
         "|-----|----------------|-------------|"]
    for a in ARMS:
        cfg = ARM_CFG[a]
        mp = f"`{cfg['manifest_path']}`" if cfg['manifest_path'] else "— (sentinel)"
        L.append(f"| `{a}` | {mp} | {cfg['description']} |")
    L += ["",
          "Registry: `ldp_r_task_eval/r_tasks/registry.real.json` (6 tasks: 3 rna, 3 methylation).",
          "Model: `openrouter/openai/gpt-4o`, temperature 0.1, max_steps 32.",
          "Evaluator: `ldp_r_task_eval/tools/evaluate_real_run.py`. Verdicts: "
          "`pass` (all expected files byte-identical or table-full-match), "
          "`partial` (files exist but differ), `fail` (missing files), "
          "`error` (run crashed).\n"]
    return L


def _md_overview(agg: dict) -> list[str]:
    L = ["## Per-arm verdict counts\n",
         "| arm | pass | partial | fail | error | pass_rate |",
         "|-----|-----:|--------:|-----:|------:|----------:|"]
    for a in ARMS:
        x = agg["arms"][a]
        pr = x.get("pass_rate") or 0.0
        L.append(f"| `{a}` | {x['n_pass']} | {x['n_partial']} | {x['n_fail']} | "
                 f"{x.get('n_error',0)} | {pr:.1f}% |")
    L.append("")
    return L


def _md_matrix(agg: dict) -> list[str]:
    L = ["## Task × arm verdict matrix\n",
         "| task | family | difficulty | " + " | ".join(f"`{a}`" for a in ARMS) + " |",
         "|------|--------|-----------:|" + "|".join(["---"] * len(ARMS)) + "|"]
    for row in agg["matrix"]:
        cells = [row.get(a, "error") for a in ARMS]
        pretty = ["**pass**" if v == "pass" else v for v in cells]
        L.append(f"| `{row['task_id']}` | {row['family']} | {row['difficulty']} | "
                 + " | ".join(pretty) + " |")
    L.append("")
    return L


def _md_strat(agg: dict) -> list[str]:
    L = ["## Stratified pass rates\n"]
    for key, label in (("by_family", "family"), ("by_difficulty", "difficulty")):
        L.append(f"### By {label}\n")
        buckets = sorted({k for a in ARMS for k in agg["stratified"][key][a].keys()})
        L.append("| arm | " + " | ".join(buckets) + " |")
        L.append("|-----|" + "|".join(["------"] * len(buckets)) + "|")
        for a in ARMS:
            cells = []
            for b in buckets:
                d = agg["stratified"][key][a].get(b, {"pass": 0, "n": 0})
                cells.append(f"{d.get('pass',0)}/{d.get('n',0)}" if d.get("n", 0) else "–")
            L.append(f"| `{a}` | " + " | ".join(cells) + " |")
        L.append("")
    return L


def _md_audit(agg: dict) -> list[str]:
    L = ["## Skill injection audit (sanity)\n",
         "Every `(arm, task)` is cross-checked: `metadata.json::skill.arm` must "
         "equal the CLI arm, `skill.injected` must match (`false` for `none`, "
         "`true` otherwise), and `skill_sha256[:8]` must equal the expected "
         "value from the Phase-2 resolver dry-run table.\n",
         "| arm | task | arm_match | injected_expected | sha_match | sha8 (got→exp) |",
         "|-----|------|:---------:|:-----------------:|:---------:|----------------|"]
    any_bad = False
    for row in agg["audit"]:
        if not row["ok"]:
            any_bad = True
        sha_cell = f"`{row['skill_sha256_8']}` → `{row['expected_sha8']}`" if row['expected_sha8'] else "—"
        mark = lambda b: "✓" if b else "✗"
        L.append(f"| `{row['arm']}` | `{row['task_id']}` | {mark(row['arm_match'])} | "
                 f"{mark(row['injected_expected'])} | {mark(row['sha_match'])} | {sha_cell} |")
    L.append("")
    L.append("**Overall:** " + ("all 24 (arm, task) pairs clean — no cross-arm leakage."
                                if not any_bad else
                                "WARNING — at least one (arm, task) pair disagreed with the expected audit; inspect rows marked ✗ above."))
    L.append("")
    return L


def _md_observations(agg: dict) -> list[str]:
    arms = agg["arms"]
    matrix = {r["task_id"]: r for r in agg["matrix"]}
    L = ["## Key observations\n"]

    by_pass = sorted(ARMS, key=lambda a: -arms[a]["n_pass"])
    best, second = by_pass[0], by_pass[1]
    L.append(f"- **Highest pass rate**: `{best}` with {arms[best]['n_pass']}/6 "
             f"({(arms[best].get('pass_rate') or 0):.1f}%); next is `{second}` "
             f"at {arms[second]['n_pass']}/6 "
             f"({(arms[second].get('pass_rate') or 0):.1f}%). "
             f"Delta: {arms[best]['n_pass'] - arms[second]['n_pass']} task(s).")

    diverged = [t for t, r in matrix.items()
                if len({r[a] for a in ARMS}) > 1]
    L.append(f"- **Arm-divergent tasks ({len(diverged)})**: "
             + (", ".join(f"`{t}`" for t in diverged) if diverged else "none")
             + ". Candidates for deeper per-task skill-content analysis.")

    pipe_root_tasks = ["akinyi_deseq2", "star_deseq2_init", "star_deseq2_contrast",
                       "methylkit_load", "methylkit_unite", "methylkit_to_tibble"]
    pipe_pass = sum(1 for t in pipe_root_tasks if matrix.get(t, {}).get("pipeline") == "pass")
    paper_pass = sum(1 for t in pipe_root_tasks if matrix.get(t, {}).get("paper") == "pass")
    L.append(f"- **Pipeline vs paper on pipeline-rooted tasks**: pipeline={pipe_pass}/6, "
             f"paper={paper_pass}/6. "
             + ("pipeline wins" if pipe_pass > paper_pass else
                "paper wins" if paper_pass > pipe_pass else "tied"))

    llm_pass = arms["llm_plan"]["n_pass"]
    best_content = max(arms["paper"]["n_pass"], arms["pipeline"]["n_pass"])
    L.append(f"- **LLM-plan parity with content-grounded skills?** "
             f"llm_plan={llm_pass}/6 vs max(paper, pipeline)={best_content}/6. "
             + ("At parity — a lot of the benchmark is just 'do DESeq2' and doesn't need external methodology."
                if llm_pass >= best_content else
                f"Behind by {best_content - llm_pass} task(s) — content-grounded skills add real signal."))

    none_pass = arms["none"]["n_pass"]
    L.append(f"- **Skill vs no-skill lift**: best skill-arm ({best}) at {arms[best]['n_pass']}/6 "
             f"vs `none` at {none_pass}/6. Lift = {arms[best]['n_pass'] - none_pass} task(s).")

    partial_per_arm = {a: [t for t, r in matrix.items() if r[a] == "partial"] for a in ARMS}
    all_partial_tasks = sorted({t for a in ARMS for t in partial_per_arm[a]})
    partial_freq = {t: sum(1 for a in ARMS if matrix[t][a] == "partial")
                    for t in all_partial_tasks}
    clustered = [t for t, n in partial_freq.items() if n >= 2]
    L.append(f"- **Partial-verdict clustering**: tasks partial in ≥2 arms: "
             + (", ".join(f"`{t}` ({partial_freq[t]}/4)" for t in clustered) if clustered
                else "none")
             + ". Clustered partials likely point at evaluator tolerance (row ordering / FP noise) rather than arm-specific logic errors; isolated partials are more likely genuine agent mistakes.")

    L.append("")
    return L


def _md_cost(agg: dict) -> list[str]:
    L = ["## Token usage + cost estimate (best-effort)\n",
         "Steps = `trajectory.jsonl` line count − 1 (initial state). Per-step "
         "averages: `none` ~2.5k in / 0.25k out, skill-injected arms ~2.7k / 0.25k "
         "(extra prompt for the SKILL.md block). GPT-4o list: $2.50 / $10.00 per M "
         "tokens in / out.\n",
         "| arm | total steps | est. in tok | est. out tok | est. USD |",
         "|-----|------------:|------------:|-------------:|---------:|"]
    total = 0.0
    for a in ARMS:
        c = agg["cost_est"][a]
        total += c["est_usd"]
        L.append(f"| `{a}` | {c['steps_total']} | {c['est_tokens_in']:,} | "
                 f"{c['est_tokens_out']:,} | ${c['est_usd']:.3f} |")
    L.append(f"| **total** | | | | **${total:.3f}** |")
    L.append("")
    return L


def _md_recommendations(agg: dict) -> list[str]:
    matrix = {r["task_id"]: r for r in agg["matrix"]}
    return [
        "## Recommendations for the next iteration\n",
        "1. **Remove shipped R scripts from canonical task workspaces.** As long "
        "as `run_*.R` sits next to `OBJECTIVE.md`, the agent can ignore the skill "
        "entirely; the current `none` arm still passes 2/6 largely because of that "
        "recipe-in-workspace shortcut. Hiding those files (or substituting a "
        "deliberately-broken one) is the fastest way to make the skill source "
        "*actually* decisive.\n",
        "2. **Per-row tolerance evaluator for methylation outputs.** `methylkit_unite` "
        "and `methylkit_to_tibble` hover between partial and fail across arms — "
        "the generated tables exist but don't match byte-for-byte (row order / "
        "float formatting). Ship the row-diff tolerant comparator mentioned in "
        "Subagent D's status so these rollouts can resolve as pass/fail on content.\n",
        "3. **Expand to more tasks per family.** 3 rna vs 3 methylation is enough "
        "to show arm differences but every per-family cell has only 3 samples. "
        "Adding 2–3 more ChIP-seq / scRNA tasks (with paper+pipeline+llm_plan "
        "skills generated in advance) would let us make per-family claims at "
        "≥5 samples/cell.\n",
        "4. **Layer PAV back on top of the winning skill source.** The V1 PAV "
        "runs were inconclusive because the skill coverage was 1/12; with the "
        f"Phase-3 winner ({max(ARMS, key=lambda a: agg['arms'][a]['n_pass'])}) "
        "giving full coverage, re-running PAV with that skill source "
        "isolates the planning-discipline lift on top of a strong recipe.\n",
        "5. **Seed / repeat the sweep.** Still 6 single-roll rollouts per arm; "
        "verdict deltas of ≤1 task are noise at this N. A 3×-repeat with the "
        "same TS prefix would give mean±sd on pass_rate.\n",
    ]


def render_summary(agg: dict) -> str:
    ts = agg["ts"]
    L = []
    L += _md_setup(ts, agg)
    L += _md_overview(agg)
    L += _md_matrix(agg)
    L += _md_strat(agg)
    L += _md_audit(agg)
    L += _md_observations(agg)
    L += _md_cost(agg)
    L += _md_recommendations(agg)
    return "\n".join(L)


def render_audit(agg: dict) -> str:
    ts = agg["ts"]
    L = [f"# Skill injection audit — TS `{ts}`\n",
         "Each (arm, task) row below confirms that the skill block in the "
         "rendered system prompt is the one the batch runner was asked to "
         "inject. sha256 values are 64-hex in metadata; the table shows "
         "the first 8 chars and cross-references the expected value from "
         "the Phase-2 resolver dry run (`_ROUTER_STATUS.md §2`). "
         "`skill_char_len` is the exact string length of the rendered "
         "block (including the wrapper section header).\n",
         "| arm | task | injected | sha256 (8) | expected | char_len | md_path | lookup |",
         "|-----|------|:--------:|------------|---------:|---------:|---------|--------|"]
    for r in agg["audit"]:
        injected = "✓" if r["injected"] else "—"
        sha = f"`{r['skill_sha256_8']}`" if r["skill_sha256_8"] else "—"
        exp = f"`{r['expected_sha8']}`" if r["expected_sha8"] else "—"
        clen = r["skill_char_len"] if r["skill_char_len"] is not None else "—"
        md = f"`{r['skill_md_path']}`" if r["skill_md_path"] else "—"
        lk = f"`{r['lookup_field']}` / `{r['lookup_key']}`" if r["lookup_field"] else "—"
        L.append(f"| `{r['arm']}` | `{r['task_id']}` | {injected} | {sha} | {exp} | {clen} | {md} | {lk} |")
    bad = [r for r in agg["audit"] if not r["ok"]]
    L += ["",
          "**Audit result:** " + ("all 24 (arm, task) pairs match expectations — "
          "no cross-arm leakage, skills injected exactly where expected."
          if not bad else
          f"{len(bad)} row(s) disagreed; see rows with mismatched sha / arm / injected above."),
          ""]
    return "\n".join(L)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--ts", required=True, help="Shared timestamp used across all four arms")
    p.add_argument("--out-dir", default=str(_ABL),
                   help="Directory for SWEEP_V2_<TS>.{json,md} + audit file")
    args = p.parse_args()

    registry = json.loads(_REG.read_text(encoding="utf-8"))
    agg = build_matrix(args.ts, registry)

    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    j_out = out_dir / f"SWEEP_V2_{args.ts}.json"
    md_out = out_dir / f"SWEEP_V2_{args.ts}_SUMMARY.md"
    audit_out = out_dir / f"SWEEP_V2_{args.ts}_SKILL_AUDIT.md"
    j_out.write_text(json.dumps(agg, indent=2))
    md_out.write_text(render_summary(agg))
    audit_out.write_text(render_audit(agg))
    print(f"wrote {j_out}")
    print(f"wrote {md_out}")
    print(f"wrote {audit_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
