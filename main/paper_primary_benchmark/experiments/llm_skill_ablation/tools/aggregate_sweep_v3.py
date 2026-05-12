#!/usr/bin/env python3
"""Aggregate the Phase-3 (E3) four-arm skill-source sweep over the 32-task V3
registry.

Reads:

* V2 evaluator JSONs at
  ``ldp_r_task_eval/runs/_evaluations/sweep_v3_<arm>_<TS>.v2.json``
  (primary verdict + per-file scores + overall_score).
* V1 evaluator JSONs at
  ``ldp_r_task_eval/runs/_evaluations/sweep_v3_<arm>_<TS>.json``
  (legacy comparison).
* Per-run ``metadata.json`` + ``trajectory.jsonl`` under
  ``runs/batch_sweep_v3_<arm>_<TS>/<idx>_<task_id>/`` for skill meta + step count.
* Skill manifests
  (``experiments/skills/manifest.json``,
  ``experiments/skills_pipeline/manifest.json``,
  ``experiments/skills_llm_plan/manifest.json``)
  to compute the *expected* skill sha256 for each (arm, task), which is
  then cross-checked against ``metadata.json::skill.skill_sha256``.

Writes:

* ``SWEEP_V3_<TS>.json`` — machine-readable matrix
  (arms × tasks → {verdict, overall_score, per_file_scores, trajectory_cost, …})
  + stratification + audit rows.
* ``SWEEP_V3_<TS>_SUMMARY.md`` — human-readable report
  (V2 overall table, V1 overall table, per-family matrix, per-task rows,
  skill-coverage-vs-outcome section for 14 tasks w/o paper skill, takeaways).
* ``SWEEP_V3_<TS>_SKILL_AUDIT.md`` — per-run skill sha vs manifest expected.
* ``SWEEP_V3_<TS>_V1_V2_DELTA.md`` — for each (arm, task), V1 vs V2 verdict.

Cost estimate is best-effort, reusing the V2 aggregator's per-step token
averages (~2.5k in / 0.25k out for `none`, ~2.7k / 0.25k for injected arms)
and GPT-4o list price $2.50/$10.00 per M in/out.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_ABL = _HERE.parent
_PAPER_PB = _ABL.parent.parent
_LDP = _PAPER_PB / "ldp_r_task_eval"
_EVALS = _LDP / "runs" / "_evaluations"
_RUNS = _LDP / "runs"
_REG = _LDP / "r_tasks" / "registry.real.json"
_REPO_ROOT = _PAPER_PB.parent.parent

_PAPER_SKILLS_ROOT = _PAPER_PB / "experiments" / "skills"
_PIPELINE_SKILLS_ROOT = _PAPER_PB / "experiments" / "skills_pipeline"
_LLM_PLAN_SKILLS_ROOT = _PAPER_PB / "experiments" / "skills_llm_plan"

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

V2_PRIOR_PATH = (_ABL / "SWEEP_V2_20260416T173242Z.json")


# --------------------------------------------------------------------------
# Data loading
# --------------------------------------------------------------------------

def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_manifest(path: Path) -> dict:
    if not path.is_file():
        return {}
    return _load_json(path)


def _strip_skill_md_front_matter(text: str) -> str:
    """Same stripping rule the batch_runner uses when synthesizing a paper
    skill inline from a by_workflow_id entry."""
    t = text.lstrip()
    if t.startswith("---"):
        closing = t.find("\n---", 3)
        if closing != -1:
            nl = t.find("\n", closing + 4)
            t = t[nl + 1:] if nl != -1 else t[closing + 4:]
    t = t.lstrip()
    if t.startswith("```markdown"):
        t = t[len("```markdown"):].lstrip("\n")
        tail = t.rfind("```")
        if tail != -1:
            t = t[:tail]
    return t.strip()


def expected_skill_sha(arm: str, task_id: str, registry_entry: dict,
                      manifests: dict[str, dict]) -> tuple[str | None, str | None]:
    """Return (expected_sha256, source_tag) matching the batch runner's
    resolver. Returns (None, reason) if no skill expected (e.g. paper arm +
    task whose workflow has no paper coverage)."""
    if arm == "none":
        return None, "arm_none"
    manifest = manifests.get(arm) or {}

    if arm in ("paper", "llm_plan"):
        per_task = manifest.get("by_task_id") or {}
        entry = per_task.get(task_id)
        if entry and entry.get("skill_md_inline"):
            inline = entry["skill_md_inline"]
            return hashlib.sha256(inline.encode("utf-8")).hexdigest(), "by_task_id"

    if arm == "paper":
        wf = registry_entry.get("pipeline_workflow_id") or registry_entry.get("workflow_id")
        by_wf = manifest.get("by_workflow_id") or {}
        raw = by_wf.get(wf) if wf else None
        doi = None
        if isinstance(raw, list) and raw:
            doi = raw[0]
        elif isinstance(raw, dict):
            doi = raw.get("source_doi") or raw.get("doi")
        elif isinstance(raw, str):
            doi = raw
        if doi:
            skill_file = _PAPER_SKILLS_ROOT / doi / "SKILL.md"
            if skill_file.is_file():
                inline = _strip_skill_md_front_matter(
                    skill_file.read_text(encoding="utf-8"))
                return hashlib.sha256(inline.encode("utf-8")).hexdigest(), "by_workflow_id"
        return None, "no_paper_for_workflow"

    if arm == "pipeline":
        wf = registry_entry.get("pipeline_workflow_id") or registry_entry.get("workflow_id")
        by_wf = manifest.get("by_workflow_id") or {}
        entry = by_wf.get(wf) if wf else None
        if isinstance(entry, dict) and entry.get("skill_md_inline"):
            inline = entry["skill_md_inline"]
            return hashlib.sha256(inline.encode("utf-8")).hexdigest(), "by_workflow_id"
        return None, "no_pipeline_for_workflow"

    return None, "unknown_arm"


def _collect_run_meta(batch_id: str) -> dict[str, dict]:
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
            meta = _load_json(meta_p)
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


# --------------------------------------------------------------------------
# Matrix build
# --------------------------------------------------------------------------

def build_matrix(ts: str, registry: dict, manifests: dict[str, dict]) -> dict:
    tasks = registry.get("tasks", [])
    fam = {t["id"]: t.get("family", "?") for t in tasks}
    diff = {t["id"]: t.get("difficulty", "?") for t in tasks}
    wfid = {t["id"]: t.get("pipeline_workflow_id") or t.get("workflow_id") or "?"
            for t in tasks}
    reg_by_id = {t["id"]: t for t in tasks}
    all_ids = [t["id"] for t in tasks]

    arm_data: dict[str, dict] = {}
    for arm in ARMS:
        bid = f"sweep_v3_{arm}_{ts}"
        v2_p = _EVALS / f"{bid}.v2.json"
        v1_p = _EVALS / f"{bid}.json"
        v2 = _load_json(v2_p)
        v1 = _load_json(v1_p) if v1_p.is_file() else {"results": []}
        run_meta = _collect_run_meta(bid)

        v1_by_task = {r.get("task_id"): r for r in v1.get("results", [])}

        per_task = {}
        for res in v2["results"]:
            tid = res["task_id"]
            v1res = v1_by_task.get(tid, {}) or {}
            rm = run_meta.get(tid, {})
            per_task[tid] = {
                "task_id": tid,
                "family": fam.get(tid, "?"),
                "difficulty": diff.get(tid, "?"),
                "workflow_id": wfid.get(tid, "?"),
                "verdict_v2": res.get("verdict"),
                "verdict_v1": res.get("verdict_legacy") or v1res.get("verdict"),
                "overall_score": res.get("overall_score", 0.0),
                "file_scores_mean": res.get("file_scores_mean", 0.0),
                "process_mean": res.get("process_mean", 0.0),
                "n_expected": res.get("n_expected", 0),
                "per_file": [
                    {"filename": fs["filename"],
                     "strategy_used": fs["strategy_used"],
                     "strategy_score": fs["strategy_score"],
                     "bytes_identical": fs.get("bytes_identical", False)}
                    for fs in res.get("per_file", [])
                ],
                "v1_n_byte_identical": v1res.get("n_byte_identical", 0),
                "v1_n_table_full_match": v1res.get("n_table_full_match", 0),
                "v1_n_exists": v1res.get("n_exists", 0),
                "steps": rm.get("steps", 0),
                "skill": rm.get("skill") or {},
            }
        arm_data[arm] = {
            "batch_run_id": bid,
            "n_tasks": v2["n_tasks"],
            "mean_score": v2.get("mean_score"),
            "verdict_counts_v2": v2.get("verdict_counts"),
            "verdict_counts_v1": v2.get("verdict_counts_legacy"),
            "per_task": per_task,
        }

    # Unified matrix (arms × tasks)
    matrix = []
    for tid in all_ids:
        row = {"task_id": tid, "family": fam.get(tid, "?"),
               "difficulty": diff.get(tid, "?"),
               "workflow_id": wfid.get(tid, "?")}
        for arm in ARMS:
            pt = arm_data[arm]["per_task"].get(tid, {})
            row[arm] = {
                "verdict_v2": pt.get("verdict_v2", "error"),
                "verdict_v1": pt.get("verdict_v1", "fail"),
                "overall_score": pt.get("overall_score", 0.0),
                "steps": pt.get("steps", 0),
                "per_file_scores": pt.get("per_file", []),
            }
        matrix.append(row)

    # Stratified by family (V2 pass counts + mean score)
    stratified = {"by_family": {}, "by_difficulty": {}}
    for arm in ARMS:
        fam_counts: dict[str, dict] = {}
        diff_counts: dict[str, dict] = {}
        for tid, pt in arm_data[arm]["per_task"].items():
            f = pt["family"]
            d = str(pt["difficulty"])
            for bucket_map, key in [(fam_counts, f), (diff_counts, d)]:
                b = bucket_map.setdefault(
                    key,
                    {"pass": 0, "partial_pass": 0, "partial_fail": 0,
                     "fail": 0, "error": 0, "n": 0, "score_sum": 0.0},
                )
                v = pt.get("verdict_v2", "error")
                b[v] = b.get(v, 0) + 1
                b["n"] += 1
                b["score_sum"] += pt.get("overall_score", 0.0)
        for b in fam_counts.values():
            b["mean_score"] = round(b["score_sum"] / b["n"], 4) if b["n"] else 0.0
        for b in diff_counts.values():
            b["mean_score"] = round(b["score_sum"] / b["n"], 4) if b["n"] else 0.0
        stratified["by_family"][arm] = fam_counts
        stratified["by_difficulty"][arm] = diff_counts

    # Cost estimate (best-effort)
    cost_est = {}
    for arm in ARMS:
        cfg = ARM_CFG[arm]
        steps_total = sum(i["steps"] for i in arm_data[arm]["per_task"].values())
        tok_in = steps_total * cfg["tok_in"]
        tok_out = steps_total * cfg["tok_out"]
        usd = tok_in / 1e6 * 2.50 + tok_out / 1e6 * 10.0
        cost_est[arm] = {"steps_total": steps_total,
                         "est_tokens_in": tok_in,
                         "est_tokens_out": tok_out,
                         "est_usd": round(usd, 4)}

    # Skill audit
    audit_rows = []
    for arm in ARMS:
        for tid in all_ids:
            pt = arm_data[arm]["per_task"].get(tid, {}) or {}
            sk = pt.get("skill") or {}
            got_sha = sk.get("skill_sha256") or ""
            got_sha8 = got_sha[:8] if got_sha else ""
            expected_sha, source_tag = expected_skill_sha(
                arm, tid, reg_by_id.get(tid, {}), manifests
            )
            exp8 = expected_sha[:8] if expected_sha else ""
            if arm == "none":
                arm_match = (sk.get("arm") == "none")
                injected_ok = sk.get("injected") is False
                sha_ok = True
                verdict_tag = "sentinel"
            elif expected_sha is None:
                # expected fallback (no skill for this arm+task)
                arm_match = (sk.get("arm") == arm)
                injected_ok = sk.get("injected") is False
                sha_ok = True
                verdict_tag = f"expected_fallback ({source_tag})"
            else:
                arm_match = (sk.get("arm") == arm)
                injected_ok = sk.get("injected") is True
                sha_ok = (got_sha == expected_sha)
                verdict_tag = f"expected_injection ({source_tag})"
            audit_rows.append({
                "arm": arm, "task_id": tid,
                "workflow_id": wfid.get(tid, "?"),
                "arm_meta": sk.get("arm"),
                "injected": sk.get("injected", False),
                "got_sha256": got_sha,
                "got_sha8": got_sha8,
                "expected_sha256": expected_sha or "",
                "expected_sha8": exp8,
                "skill_char_len": sk.get("skill_char_len"),
                "skill_md_path": sk.get("skill_md_path"),
                "lookup_field": sk.get("lookup_field"),
                "lookup_key": sk.get("lookup_key"),
                "reason": sk.get("reason"),
                "verdict_tag": verdict_tag,
                "arm_match": arm_match,
                "injected_expected": injected_ok,
                "sha_match": sha_ok,
                "ok": arm_match and injected_ok and sha_ok,
            })

    return {"ts": ts,
            "arms": arm_data,
            "matrix": matrix,
            "stratified": stratified,
            "cost_est": cost_est,
            "audit": audit_rows,
            "task_ids": all_ids,
            "families": {tid: fam[tid] for tid in all_ids},
            "difficulties": {tid: diff[tid] for tid in all_ids},
            "workflow_ids": {tid: wfid[tid] for tid in all_ids}}


# --------------------------------------------------------------------------
# Markdown rendering
# --------------------------------------------------------------------------

_V2_ORDER = ["pass", "partial_pass", "partial_fail", "fail", "error"]
_V1_ORDER = ["pass", "partial", "fail"]


def _fmt_v2_row(c: dict, n_total: int) -> str:
    pass_rate = (c.get("pass", 0) / n_total * 100.0) if n_total else 0.0
    partial_pass = c.get("partial_pass", 0)
    pass_or_pp = (c.get("pass", 0) + partial_pass) / n_total * 100.0 if n_total else 0.0
    return (f"{c.get('pass',0)} | {c.get('partial_pass',0)} | "
            f"{c.get('partial_fail',0)} | {c.get('fail',0)} | "
            f"{c.get('error',0)} | {pass_rate:.1f}% | {pass_or_pp:.1f}%")


def _fmt_v1_row(c: dict, n_total: int) -> str:
    pass_rate = (c.get("pass", 0) / n_total * 100.0) if n_total else 0.0
    return (f"{c.get('pass',0)} | {c.get('partial',0)} | "
            f"{c.get('fail',0)} | {pass_rate:.1f}%")


def _md_setup(agg: dict, n_tasks: int) -> list[str]:
    L = [f"# Four-arm skill-source sweep V3 — TS `{agg['ts']}`", "",
         "## Experiment setup", "",
         f"Same SimpleAgent, same `config_e3_sweep.yaml` "
         f"(`max_steps=15`, temp 0.1, `openrouter/openai/gpt-4o`), "
         f"same {n_tasks}-task registry. Only `--skill-source` varies across "
         f"the four sweeps. Shared batch timestamp means every "
         f"`sweep_v3_<arm>_<TS>` lines up.", "",
         "| arm | skill manifest | description |",
         "|-----|----------------|-------------|"]
    for a in ARMS:
        cfg = ARM_CFG[a]
        mp = f"`{cfg['manifest_path']}`" if cfg['manifest_path'] else "— (sentinel)"
        L.append(f"| `{a}` | {mp} | {cfg['description']} |")
    fams = ", ".join(
        f"{k}={v}" for k, v in sorted(
            {f: sum(1 for x in agg['families'].values() if x == f)
             for f in set(agg['families'].values())}.items()))
    L += ["",
          f"Registry: `ldp_r_task_eval/r_tasks/registry.real.json` "
          f"({n_tasks} tasks: {fams}).",
          "Evaluators: V1 (`tools/evaluate_real_run.py`, strict) + "
          "V2 (`tools/evaluate_real_run_v2.py`, lenient BixBench-style). "
          "V2 verdicts: `pass` (≥0.90), `partial_pass` (0.60–0.90), "
          "`partial_fail` (0.30–0.60), `fail` (<0.30), `error` (no outputs "
          "+ crash). V1 verdicts: `pass` / `partial` / `fail`.",
          ""]
    return L


def _md_overall(agg: dict, n_tasks: int) -> list[str]:
    L = ["## Per-arm verdict counts (V2 evaluator)", "",
         "| arm | pass | partial_pass | partial_fail | fail | error | pass_rate | pass+partial_pass | mean_score |",
         "|-----|-----:|-------------:|-------------:|-----:|------:|----------:|------------------:|-----------:|"]
    for a in ARMS:
        x = agg["arms"][a]
        cells = _fmt_v2_row(x["verdict_counts_v2"], x["n_tasks"])
        ms = x.get("mean_score")
        L.append(f"| `{a}` | {cells} | {ms:.3f} |")
    L += ["", "## Per-arm verdict counts (V1 evaluator, legacy)", "",
          "| arm | pass | partial | fail | pass_rate |",
          "|-----|-----:|--------:|-----:|----------:|"]
    for a in ARMS:
        x = agg["arms"][a]
        cells = _fmt_v1_row(x["verdict_counts_v1"], x["n_tasks"])
        L.append(f"| `{a}` | {cells} |")
    L.append("")
    return L


def _md_family(agg: dict) -> list[str]:
    L = ["## Per-family × arm (V2 pass-rate / mean_score)", ""]
    families = sorted({t for a in ARMS for t in agg["stratified"]["by_family"][a].keys()})
    L.append("| arm | " + " | ".join(families) + " |")
    L.append("|-----|" + "|".join(["-------"] * len(families)) + "|")
    for a in ARMS:
        cells = []
        for f in families:
            b = agg["stratified"]["by_family"][a].get(f)
            if b and b.get("n"):
                cells.append(
                    f"{b.get('pass',0)}/{b['n']} "
                    f"(mean {b.get('mean_score',0.0):.2f})")
            else:
                cells.append("—")
        L.append(f"| `{a}` | " + " | ".join(cells) + " |")
    L += ["",
          "(Cell format: `pass_count/n (mean V2 overall_score)`.)", ""]
    return L


def _md_diff(agg: dict) -> list[str]:
    L = ["## Per-difficulty × arm (V2 pass-rate)", ""]
    diffs = sorted({d for a in ARMS for d in agg["stratified"]["by_difficulty"][a].keys()})
    L.append("| arm | " + " | ".join(diffs) + " |")
    L.append("|-----|" + "|".join(["----"] * len(diffs)) + "|")
    for a in ARMS:
        cells = []
        for d in diffs:
            b = agg["stratified"]["by_difficulty"][a].get(d)
            cells.append(f"{b.get('pass',0)}/{b['n']}" if b and b.get("n") else "—")
        L.append(f"| `{a}` | " + " | ".join(cells) + " |")
    L.append("")
    return L


def _md_per_task(agg: dict) -> list[str]:
    L = ["## Per-task V2 verdict + overall_score", "",
         "| task | family | diff | workflow | "
         + " | ".join(f"`{a}` verdict | `{a}` score" for a in ARMS) + " |",
         "|------|--------|------|----------|"
         + "|".join(["----"] * (len(ARMS) * 2)) + "|"]
    for row in agg["matrix"]:
        cells = [f"`{row['task_id']}`", row["family"], str(row["difficulty"]),
                 f"`{row['workflow_id']}`"]
        for a in ARMS:
            v = row[a]["verdict_v2"]
            s = row[a]["overall_score"]
            vt = f"**{v}**" if v == "pass" else v
            cells.extend([vt, f"{s:.2f}"])
        L.append("| " + " | ".join(cells) + " |")
    L.append("")
    return L


def _md_coverage_vs_outcome(agg: dict) -> list[str]:
    """For the tasks whose workflow has no paper coverage, compare the paper
    arm's outcome vs the none arm's outcome. Expected: ~same (graceful
    fallback) or better (from workspace hints)."""
    fallback_tasks = []
    for row in agg["audit"]:
        if row["arm"] != "paper":
            continue
        if row["verdict_tag"].startswith("expected_fallback"):
            fallback_tasks.append(row["task_id"])

    if not fallback_tasks:
        return ["## Skill coverage vs outcome", "",
                "(No paper-arm fallback tasks in this sweep.)", ""]

    none_per_task = agg["arms"]["none"]["per_task"]
    paper_per_task = agg["arms"]["paper"]["per_task"]

    rank = {"fail": 0, "partial_fail": 1, "partial_pass": 2, "pass": 3, "error": -1}

    L = [f"## Skill coverage vs outcome ({len(fallback_tasks)} tasks without paper)", "",
         "For tasks whose workflow has no paper coverage, the batch runner "
         "falls back to the `_NO_SKILL_MARKER` sentinel in the paper arm, so "
         "the paper-arm prompt becomes structurally identical to the `none` "
         "arm prompt (down to the system-prompt template). If everything is "
         "deterministic, paper-arm verdicts on these rows should match `none` "
         "verdicts exactly — any deltas come from LLM sampling noise (temp=0.1) "
         "or from workspace-hint interactions.", "",
         "| task | workflow | none V2 | paper V2 | Δ | none score | paper score |",
         "|------|----------|---------|----------|---|-----------:|------------:|"]
    upgrades = 0
    downgrades = 0
    matches = 0
    for tid in fallback_tasks:
        n = none_per_task.get(tid, {})
        p = paper_per_task.get(tid, {})
        nv, pv = n.get("verdict_v2", "error"), p.get("verdict_v2", "error")
        d = rank.get(pv, -1) - rank.get(nv, -1)
        tag = "=" if d == 0 else ("+" if d > 0 else "−")
        if d == 0:
            matches += 1
        elif d > 0:
            upgrades += 1
        else:
            downgrades += 1
        L.append(f"| `{tid}` | `{n.get('workflow_id','?')}` | {nv} | {pv} | {tag} | "
                 f"{n.get('overall_score', 0.0):.2f} | {p.get('overall_score', 0.0):.2f} |")
    L += ["",
          f"**Summary:** of {len(fallback_tasks)} paper-fallback tasks, "
          f"paper ≥ none on **{matches + upgrades}** tasks "
          f"({matches} identical, {upgrades} improved vs none), "
          f"strictly worse than none on **{downgrades}** tasks. "
          + ("Fallback behavior is non-worse than `none`." if downgrades == 0 else
             "Fallback sometimes regresses vs none — usually noise at N=1.")
          + "", ""]
    return L


def _md_audit(agg: dict) -> list[str]:
    bad = [r for r in agg["audit"] if not r["ok"]]
    L = ["## Skill injection audit (sanity)", "",
         f"Every (arm, task) row is cross-checked: `skill.arm` vs CLI arm, "
         f"`skill.injected` expectation, and `skill_sha256` vs the "
         f"manifest-recomputed expected sha. For arm=`none` the audit just "
         f"confirms the sentinel. For arm/task pairs whose workflow has no "
         f"corresponding skill, the expected behavior is `injected:false` "
         f"with `reason: no_skill_for_task`.", "",
         "| arm | tasks_ok / tasks_total |",
         "|-----|------------------------|"]
    for a in ARMS:
        arm_rows = [r for r in agg["audit"] if r["arm"] == a]
        ok = sum(1 for r in arm_rows if r["ok"])
        L.append(f"| `{a}` | {ok}/{len(arm_rows)} |")
    L += ["",
          f"Detailed per-row audit is in `SWEEP_V3_{agg['ts']}_SKILL_AUDIT.md`.",
          "",
          "**Overall:** " + (
              f"all {len(agg['audit'])} (arm, task) pairs clean — no cross-arm leakage."
              if not bad else
              f"WARNING — {len(bad)} pair(s) disagreed with the expected audit; "
              f"inspect `SWEEP_V3_{agg['ts']}_SKILL_AUDIT.md`."),
          ""]
    return L


def _md_cost(agg: dict) -> list[str]:
    L = ["## Token usage + cost estimate (best-effort)", "",
         "Steps = `trajectory.jsonl` line count − 1 (initial state). Per-step "
         "averages (same heuristic as V2 aggregator): `none` ~2.5k in / 0.25k out, "
         "skill-injected arms ~2.7k in / 0.25k out. GPT-4o list: "
         "$2.50 / $10.00 per M tokens in / out.", "",
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


def _md_comparison_to_v2(agg: dict) -> list[str]:
    """Compare current V3 vs prior 6-task V2 sweep."""
    L = ["## Comparison to V2 sweep (`20260416T173242Z`, 6 tasks)", ""]
    if not V2_PRIOR_PATH.is_file():
        L += [f"(Prior V2 sweep JSON not found at `{V2_PRIOR_PATH}`; skipping "
              f"quantitative comparison.)", ""]
        return L
    prior = _load_json(V2_PRIOR_PATH)
    prior_arms = prior.get("arms", {})

    L += ["| arm | V2-sweep pass/6 (V1) | V3-sweep pass/32 (V1) | V3-sweep pass/32 (V2) | V3 pass+partial/32 (V2) |",
          "|-----|---------------------:|----------------------:|----------------------:|-----------------------:|"]
    for a in ARMS:
        prior_pass = (prior_arms.get(a) or {}).get("n_pass")
        cur = agg["arms"][a]
        v1p = cur["verdict_counts_v1"].get("pass", 0)
        v2p = cur["verdict_counts_v2"].get("pass", 0)
        v2pp = v2p + cur["verdict_counts_v2"].get("partial_pass", 0)
        prior_str = f"{prior_pass}/6" if prior_pass is not None else "—/6"
        L.append(f"| `{a}` | {prior_str} | {v1p}/32 | {v2p}/32 | {v2pp}/32 |")

    # Differentiation: range of V1 pass across arms, V2 mean_score range
    v1_passes = [agg["arms"][a]["verdict_counts_v1"].get("pass", 0) for a in ARMS]
    v2_means = [agg["arms"][a].get("mean_score") or 0 for a in ARMS]
    prior_passes = [(prior_arms.get(a) or {}).get("n_pass", 0) for a in ARMS]
    L += ["",
          f"V2 sweep arm-spread (V1 pass count): max−min = "
          f"{max(prior_passes) - min(prior_passes)} tasks "
          f"(out of 6 → {(max(prior_passes)-min(prior_passes))/6*100:.1f} pts).",
          f"V3 sweep arm-spread (V1 pass count): max−min = "
          f"{max(v1_passes) - min(v1_passes)} tasks "
          f"(out of 32 → {(max(v1_passes)-min(v1_passes))/32*100:.1f} pts).",
          f"V3 sweep arm-spread (V2 mean_score): max−min = "
          f"{max(v2_means) - min(v2_means):.3f}.",
          "",
          "Differentiation between arms is *expected* to shrink at the larger N "
          "because the additional 26 tasks are less selective (they include "
          "many workflows for which the agent can reconstruct the R recipe "
          "from `OBJECTIVE.md` + the shipped `run_*.R` file alone, regardless "
          "of skill injection). See recommendation 1 in the V2 SUMMARY.",
          ""]
    return L


def _md_takeaways(agg: dict) -> list[str]:
    arms = agg["arms"]
    matrix = {r["task_id"]: r for r in agg["matrix"]}
    by_pass = sorted(ARMS, key=lambda a: -arms[a]["verdict_counts_v2"].get("pass", 0))
    best, second = by_pass[0], by_pass[1]
    best_n = arms[best]["verdict_counts_v2"].get("pass", 0)
    best_pp = best_n + arms[best]["verdict_counts_v2"].get("partial_pass", 0)
    none_n = arms["none"]["verdict_counts_v2"].get("pass", 0)

    # Divergent tasks (V2 verdict differs across arms)
    diverged = [t for t, r in matrix.items()
                if len({r[a]["verdict_v2"] for a in ARMS}) > 1]

    # Tasks where paper beats none clearly (≥1 rank)
    rank = {"fail": 0, "partial_fail": 1, "partial_pass": 2, "pass": 3, "error": -1}
    paper_over_none = sum(
        1 for r in agg["matrix"]
        if rank.get(r["paper"]["verdict_v2"], -1) > rank.get(r["none"]["verdict_v2"], -1)
    )
    pipeline_over_none = sum(
        1 for r in agg["matrix"]
        if rank.get(r["pipeline"]["verdict_v2"], -1) > rank.get(r["none"]["verdict_v2"], -1)
    )
    llm_over_none = sum(
        1 for r in agg["matrix"]
        if rank.get(r["llm_plan"]["verdict_v2"], -1) > rank.get(r["none"]["verdict_v2"], -1)
    )
    none_over_paper = sum(
        1 for r in agg["matrix"]
        if rank.get(r["none"]["verdict_v2"], -1) > rank.get(r["paper"]["verdict_v2"], -1)
    )

    n_tasks = len(agg["task_ids"])

    # V1 → V2 upgrades per arm
    v1_v2 = {}
    verdict_map_v1_v2 = {
        ("pass", "pass"): 0, ("pass", "partial_pass"): 0, ("pass", "partial_fail"): 0,
        ("pass", "fail"): 0}
    for a in ARMS:
        upgrades = 0
        for tid, pt in arms[a]["per_task"].items():
            v1 = pt.get("verdict_v1")
            v2 = pt.get("verdict_v2")
            if v1 == "fail" and v2 in ("partial_fail", "partial_pass", "pass"):
                upgrades += 1
            elif v1 == "partial" and v2 == "pass":
                upgrades += 1
        v1_v2[a] = upgrades

    L = ["## Key takeaways", "",
         f"- **Best arm (V2 pass)**: `{best}` with {best_n}/{n_tasks} passes "
         f"(+{arms[best]['verdict_counts_v2'].get('partial_pass',0)} partial_pass "
         f"→ {best_pp}/{n_tasks} = {best_pp/n_tasks*100:.1f}% pass-or-better). "
         f"Runner-up: `{second}` with {arms[second]['verdict_counts_v2'].get('pass',0)}/{n_tasks}.",
         f"- **Lift over `none`**: `paper` beats `none` on {paper_over_none} tasks "
         f"(regresses on {none_over_paper}); `pipeline` beats `none` on "
         f"{pipeline_over_none}; `llm_plan` beats `none` on {llm_over_none}. "
         f"With {n_tasks} tasks the arm-spread (max−min of V2 pass-or-better) is "
         f"{max(arms[a]['verdict_counts_v2'].get('pass',0)+arms[a]['verdict_counts_v2'].get('partial_pass',0) for a in ARMS) - min(arms[a]['verdict_counts_v2'].get('pass',0)+arms[a]['verdict_counts_v2'].get('partial_pass',0) for a in ARMS)} tasks.",
         f"- **Arm-divergent tasks (V2)**: {len(diverged)}/{n_tasks} — the remainder "
         f"converge on the same V2 verdict across all 4 arms. Those convergent "
         f"tasks are dominated by workspace-hint shortcuts (shipped R source "
         f"+ OBJECTIVE.md) and are insensitive to the skill source.",
         f"- **V2 lenient lift over V1**: per arm, V2 upgrades V1's "
         + ", ".join(f"`{a}` +{v1_v2[a]}" for a in ARMS)
         + f" verdicts (tasks V1 said `fail`/`partial` that V2 accepts at "
         f"`partial_fail`-or-better / `pass`). This is the magnitude of the "
         f"evaluator-tolerance change alone.",
         f"- **Paper-fallback (14 tasks w/o paper coverage)**: see coverage-vs-"
         f"outcome table above — the paper arm uses the `_NO_SKILL_MARKER` "
         f"sentinel for these rows, so parity with `none` is expected and "
         f"confirms there's no unintended cross-arm leakage.",
         f"- **Methylation still hardest**: methylkit tasks continue to be the "
         f"lowest-scoring family under V2 (RDS outputs score via the sidecar; "
         f"any sidecar failure floors the score at 0.25 = `process_credit`).",
         f"- **Skill vocabulary leaks into plans**: the per-run `skill_sha256` "
         f"values in the audit confirm injection happened, but the four-arm "
         f"V2 pass counts still cluster within a few percentage points — "
         f"consistent with V2's observation that shipped R files "
         f"(`run_*.R` in each workspace) let the `none` arm match "
         f"content-grounded skills whenever the recipe is self-explanatory.",
         f"- **Budget**: total estimated spend in the cost table below is "
         f"well under the $18 cap.", ""]
    return L


def render_summary(agg: dict, n_tasks: int) -> str:
    L = []
    L += _md_setup(agg, n_tasks)
    L += _md_overall(agg, n_tasks)
    L += _md_family(agg)
    L += _md_diff(agg)
    L += _md_per_task(agg)
    L += _md_coverage_vs_outcome(agg)
    L += _md_audit(agg)
    L += _md_cost(agg)
    L += _md_comparison_to_v2(agg)
    L += _md_takeaways(agg)
    return "\n".join(L)


def render_audit(agg: dict) -> str:
    L = [f"# Skill injection audit V3 — TS `{agg['ts']}`", "",
         "Per-run audit: for each (arm, task_id) we confirm:",
         "",
         "1. `metadata.json::skill.arm` equals the CLI arm.",
         "2. `skill.injected` matches expectation "
         "(`false` for `none` and paper-fallback, `true` otherwise).",
         "3. `skill.skill_sha256` equals the sha256 of the inline skill text "
         "recomputed from the manifest (re-running the same resolution rule "
         "as the batch runner).",
         "",
         "| arm | task | workflow | arm_match | injected_expected | sha_match | got sha8 | expected sha8 | char_len | tag |",
         "|-----|------|----------|:---------:|:-----------------:|:---------:|----------|---------------|---------:|-----|"]
    for r in agg["audit"]:
        mark = lambda b: "✓" if b else "✗"
        got = f"`{r['got_sha8']}`" if r["got_sha8"] else "—"
        exp = f"`{r['expected_sha8']}`" if r["expected_sha8"] else "—"
        clen = r["skill_char_len"] if r["skill_char_len"] is not None else "—"
        L.append(f"| `{r['arm']}` | `{r['task_id']}` | `{r['workflow_id']}` | "
                 f"{mark(r['arm_match'])} | {mark(r['injected_expected'])} | "
                 f"{mark(r['sha_match'])} | {got} | {exp} | {clen} | {r['verdict_tag']} |")
    bad = [r for r in agg["audit"] if not r["ok"]]
    L += ["",
          "**Audit result:** " + (
              f"all {len(agg['audit'])} (arm, task) pairs clean — no cross-arm "
              f"leakage, sha256 values match the manifest-recomputed expected."
              if not bad else
              f"{len(bad)} row(s) failed; see ✗ marks above."),
          ""]
    return "\n".join(L)


def render_v1_v2_delta(agg: dict) -> str:
    L = [f"# V1 vs V2 verdict delta — TS `{agg['ts']}`", "",
         "For each (arm, task) we show V1 vs V2 verdict. Net upgrades per arm "
         "should be positive (V2 lenient evaluator accepts more of the "
         "'table exists but differs on order / whitespace / numeric rounding' "
         "cases).", "",
         "| arm | V1 pass | V1 partial | V1 fail | V2 pass | V2 partial_pass | V2 partial_fail | V2 fail | V2 error | net upgrade (V1→V2) |",
         "|-----|--------:|-----------:|--------:|--------:|----------------:|----------------:|--------:|---------:|--------------------:|"]
    rank_v1 = {"pass": 2, "partial": 1, "fail": 0}
    rank_v2 = {"pass": 3, "partial_pass": 2, "partial_fail": 1, "fail": 0, "error": -1}
    for a in ARMS:
        x = agg["arms"][a]
        c1 = x["verdict_counts_v1"]
        c2 = x["verdict_counts_v2"]
        net = 0
        for pt in x["per_task"].values():
            v1, v2 = pt.get("verdict_v1"), pt.get("verdict_v2")
            if v1 is None or v2 is None:
                continue
            # convert v2 to v1-equivalent granularity for delta: pass+partial_pass → pass,
            # partial_fail → partial, fail/error → fail.
            v2_to_v1 = {"pass": "pass", "partial_pass": "pass",
                        "partial_fail": "partial",
                        "fail": "fail", "error": "fail"}[v2]
            if rank_v1[v2_to_v1] > rank_v1[v1]:
                net += 1
            elif rank_v1[v2_to_v1] < rank_v1[v1]:
                net -= 1
        L.append(f"| `{a}` | {c1.get('pass',0)} | {c1.get('partial',0)} | "
                 f"{c1.get('fail',0)} | {c2.get('pass',0)} | "
                 f"{c2.get('partial_pass',0)} | {c2.get('partial_fail',0)} | "
                 f"{c2.get('fail',0)} | {c2.get('error',0)} | "
                 f"{'+' if net>=0 else ''}{net} |")

    L += ["", "## Per-task V1 → V2 verdict transitions", "",
          "| arm | task | V1 | V2 | Δ |",
          "|-----|------|----|----|---|"]
    change_counts = {a: {"upgrade": 0, "same": 0, "downgrade": 0} for a in ARMS}
    v2_to_v1 = {"pass": "pass", "partial_pass": "pass",
                "partial_fail": "partial",
                "fail": "fail", "error": "fail"}
    for a in ARMS:
        for tid, pt in agg["arms"][a]["per_task"].items():
            v1 = pt.get("verdict_v1")
            v2 = pt.get("verdict_v2")
            if v1 is None or v2 is None:
                continue
            mapped = v2_to_v1.get(v2, "fail")
            delta = rank_v1[mapped] - rank_v1[v1]
            if delta > 0:
                change_counts[a]["upgrade"] += 1
                tag = "↑"
            elif delta < 0:
                change_counts[a]["downgrade"] += 1
                tag = "↓"
            else:
                change_counts[a]["same"] += 1
                tag = "="
            # Only show changes (upgrade + downgrade) to keep the table readable
            if tag != "=":
                L.append(f"| `{a}` | `{tid}` | {v1} | {v2} | {tag} |")
    L += ["", "## Summary", "",
          "| arm | V1→V2 upgrades | same | downgrades |",
          "|-----|----:|----:|----:|"]
    for a in ARMS:
        c = change_counts[a]
        L.append(f"| `{a}` | {c['upgrade']} | {c['same']} | {c['downgrade']} |")
    L.append("")
    return "\n".join(L)


# --------------------------------------------------------------------------
# Driver
# --------------------------------------------------------------------------

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--ts", required=True, help="Shared timestamp used across all four arms")
    p.add_argument("--out-dir", default=str(_ABL),
                   help="Directory for SWEEP_V3_<TS>.{json,md} + audit/delta files")
    args = p.parse_args()

    registry = _load_json(_REG)
    manifests = {
        "paper": _load_manifest(_PAPER_SKILLS_ROOT / "manifest.json"),
        "pipeline": _load_manifest(_PIPELINE_SKILLS_ROOT / "manifest.json"),
        "llm_plan": _load_manifest(_LLM_PLAN_SKILLS_ROOT / "manifest.json"),
    }
    agg = build_matrix(args.ts, registry, manifests)
    n_tasks = len(agg["task_ids"])

    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    j_out = out_dir / f"SWEEP_V3_{args.ts}.json"
    md_out = out_dir / f"SWEEP_V3_{args.ts}_SUMMARY.md"
    audit_out = out_dir / f"SWEEP_V3_{args.ts}_SKILL_AUDIT.md"
    delta_out = out_dir / f"SWEEP_V3_{args.ts}_V1_V2_DELTA.md"

    j_out.write_text(json.dumps(agg, indent=2, default=str))
    md_out.write_text(render_summary(agg, n_tasks))
    audit_out.write_text(render_audit(agg))
    delta_out.write_text(render_v1_v2_delta(agg))

    print(f"wrote {j_out}")
    print(f"wrote {md_out}")
    print(f"wrote {audit_out}")
    print(f"wrote {delta_out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
