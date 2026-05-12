#!/usr/bin/env python3
"""Build SKILL_COVERAGE_V3 matrix + total costs."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REG = json.loads((ROOT / "ldp_r_task_eval" / "r_tasks" / "registry.real.json").read_text())
paper = json.loads((ROOT / "experiments" / "skills" / "manifest.json").read_text())
pipeline = json.loads((ROOT / "experiments" / "skills_pipeline" / "manifest.json").read_text())
llm = json.loads((ROOT / "experiments" / "skills_llm_plan" / "manifest.json").read_text())

OUT = ROOT / "experiments" / "llm_skill_ablation" / "SKILL_COVERAGE_V3.md"

lines = [
    "# Skill coverage matrix — V3",
    "",
    f"Generated from manifests at 2026-04-17. Tasks: {len(REG['tasks'])}.",
    "",
    f"- Paper manifest version: {paper.get('version')} | by_workflow_id: {len(paper.get('by_workflow_id', {}))} | by_task_id: {len(paper.get('by_task_id', {}))}",
    f"- Pipeline manifest version: {pipeline.get('version')} | by_workflow_id: {len(pipeline.get('by_workflow_id', {}))}",
    f"- LLM-plan manifest version: {llm.get('version')} | by_task_id: {len(llm.get('by_task_id', {}))}",
    "",
    "| task_id | workflow_id | has_paper | has_pipeline | has_llm_plan |",
    "|---|---|---|---|---|",
]

n_paper = 0
n_pipeline = 0
n_llm = 0
missing_pipeline = []
missing_llm = []
missing_paper = []

for t in REG["tasks"]:
    tid = t["id"]
    wid = t["pipeline_workflow_id"]
    hp = "Y" if tid in paper.get("by_task_id", {}) or wid in paper.get("by_workflow_id", {}) else "N"
    hpipe = "Y" if wid in pipeline.get("by_workflow_id", {}) else "N"
    hllm = "Y" if tid in llm.get("by_task_id", {}) else "N"
    if hp == "Y":
        n_paper += 1
    else:
        missing_paper.append(f"{tid} ({wid})")
    if hpipe == "Y":
        n_pipeline += 1
    else:
        missing_pipeline.append(f"{tid} ({wid})")
    if hllm == "Y":
        n_llm += 1
    else:
        missing_llm.append(f"{tid} ({wid})")
    lines.append(f"| {tid} | {wid} | {hp} | {hpipe} | {hllm} |")

lines += [
    "",
    f"## Summary",
    f"- Tasks with paper skill: {n_paper}/{len(REG['tasks'])}",
    f"- Tasks with pipeline skill: {n_pipeline}/{len(REG['tasks'])}",
    f"- Tasks with llm_plan skill: {n_llm}/{len(REG['tasks'])}",
    "",
    f"## Missing paper coverage ({len(missing_paper)} tasks)",
    "Expected for workflows whose primary_doi is null or whose PDF C3 could "
    "not download (single-cell-rna-seq-finish, epigen-spilterlize_integrate-finish, "
    "snakemake-workflows-chipseq-finish, snakemake-workflows-rna-longseq-de-isoform, "
    "RiyaDua-cervical-cancer-snakemake-workflow, joncahn-epigeneticbutton-finish).",
    "",
]
for m in missing_paper:
    lines.append(f"- {m}")

lines += [
    "",
    f"## Bug: tasks missing pipeline skill ({len(missing_pipeline)})",
]
for m in missing_pipeline:
    lines.append(f"- {m}")

lines += [
    "",
    f"## Bug: tasks missing llm_plan skill ({len(missing_llm)})",
]
for m in missing_llm:
    lines.append(f"- {m}")

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text("\n".join(lines) + "\n")
print(f"wrote {OUT}")
print(f"paper={n_paper} pipeline={n_pipeline} llm={n_llm}")
