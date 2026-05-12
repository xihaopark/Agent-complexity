# Coordination Plan — Real-Task Expansion + Paper2Skills + Flexible Agent

Goal: scale real R-task benchmark and rerun a meaningful no-skill vs with-skill
comparison, with a more flexible agent architecture (plan → act → verify) and a
properly-converted skill set from the downloaded method papers.

## Current state (before this plan)

- 4 real tasks (`akinyi_deseq2`, `riya_limma`, `snakepipes_merge_fc`,
  `snakepipes_merge_ct`) under `ldp_r_task_eval/tasks/real/`, ground truth
  isolated at `ldp_r_task_eval/tasks/real_ground_truth/`.
- 7 / 22 DOIs resolved to open-access PDFs under `literature/pdfs/`.
- SimpleAgent with `openrouter/openai/gpt-4o`, max_steps=32.
- Evaluator: `tools/evaluate_real_run.py` — sha256 + per-cell numeric
  tolerance.
- Two methods for skill creation are available but not yet compared:
  - `external/Paper2Skills/` — agentic vision pipeline (reads PDF pages as
    images, writes Python skill modules with tests via LangGraph).
  - `literature/tools/paper_to_skill.py` — simple DOI metadata → markdown
    template (no paper understanding).

## Workstreams

### A. Task Expansion — proportional sampling by stage × difficulty

Owner: Subagent A (read-write).

Expand from 4 to ~20 real tasks by:

1. Enumerate every R script under `main/finish/workflow_candidates/**/*.R`
   that uses `commandArgs(trailingOnly=TRUE)` (can run standalone) OR can be
   trivially wrapped.
2. Classify each candidate by:
   - **workflow family** (rna / chipseq / atacseq / methyl / scrna / variant)
   - **stage position** (early: QC/merge → mid: normalization/filter → late:
     DE/enrichment/plot)
   - **difficulty** (1 = base-R merge/reshape, 2 = limma/DESeq2 DE, 3 =
     multi-step DE + filtering + plotting, 4 = scRNA Seurat/scran pipelines)
   - **has paper** (is this workflow_id in `literature/workflow_literature_map.json`?)
3. Sample ~20 tasks with:
   - Coverage of at least 4 families
   - Coverage of early/mid/late stages (roughly equal)
   - Difficulty distribution: ~6 easy, ~10 medium, ~4 hard
   - **Prioritize** tasks whose workflow has a paper (ideally a downloaded PDF)
4. For each sampled R script, add a TaskSpec to
   `ldp_r_task_eval/tools/build_real_r_tasks.py` that generates realistic
   synthetic inputs and runs the script against them.
5. Build + validate all tasks (`--all --force`) and update
   `r_tasks/registry.real.json`.

Dependencies available in local R 4.5.1: DESeq2, limma, ggplot2, dplyr, tidyr,
readr, pheatmap, rmarkdown, stringr, scales. **NOT** available: tidyverse
(meta-package), Seurat, EnhancedVolcano, scater, scran, edgeR. Do NOT pick
scripts whose library imports require missing packages.

### B. Paper2Skills Method Comparison

Owner: Subagent B (read-write).

Compare the two methods on the same set of 2 downloaded PDFs (pick one DESeq2
paper + one systemPipeR/kallisto paper from `literature/pdfs/`):

1. Run `external/Paper2Skills/run_skill_creator.py` (or a CLI wrapper) with
   the target PDFs and save outputs under
   `main/paper_primary_benchmark/experiments/paper2skills_ab_test/vision_out/<doi>/`.
2. Run `literature/tools/paper_to_skill.py` on the same DOIs; save outputs
   under `.../template_out/<doi>/`.
3. Produce a report `comparison.md` comparing:
   - Runtime + API cost (tokens).
   - Depth of generated skill (method coverage, executable code, citations).
   - Usability for agent context (can this be dropped into the with-skill
     system prompt? is it a full SKILL.md + scripts package?).
   - Recommendation: which approach to use for producing skills for the
     with-skill arm.

If `external/Paper2Skills` has env/dependency blockers (Azure keys, LangGraph
deps), document those. Do NOT invest more than 30 minutes trying to make it
run; if blocked, say so and benchmark just the template method, with a
qualitative review of what the vision pipeline *would* add based on its code.

### C. Flexible Agent Architecture

Owner: Subagent C (read-write).

Current agent: `ldp.agent.simple_agent.SimpleAgent` — one action per step,
implicit loop, no dedicated plan/reflect.

Make the agent plan → act → verify on each step:

1. Add two new tools to `RTaskEvalEnv` (or to a tiny "planner wrapper"):
   - `write_plan(plan: str)` — persists to `workspace/.plan.md`.
   - `check_progress(note: str)` — appends to `workspace/.progress.log`, also
     returns a terse snapshot of `output/` + remaining deliverables.
2. Update the system prompt in a **new** config file
   `experiments/llm_skill_ablation/config_llm_plan_act_verify.yaml` that
   instructs the agent to:
   - First call `write_plan` with a bullet list.
   - Then execute steps one at a time, invoking `check_progress` after any
     non-trivial change.
   - Before `submit_done`, call `list_workdir` + `check_progress` to verify
     deliverables exist.
3. Keep the old configs intact so we can compare plan-act-verify vs vanilla.
4. Run one smoke-test on `akinyi_deseq2` to verify the new loop works
   end-to-end.

### D. Skill Generation (after B recommends)

Owner: I (coordinator) assemble after B is done.

Generate skills for the 7 downloaded DOIs using the winning method, store
under `experiments/skills/<doi>/SKILL.md` (+ scripts if vision method), and
wire them into the with-skill system prompt.

### E. Experiment Orchestration (after A+C+D)

Owner: I (coordinator).

Run four arms on the expanded registry:
- scripted (smoke)
- LLM vanilla no-skill
- LLM vanilla with-skill
- LLM plan-act-verify with-skill

Evaluate with `tools/evaluate_real_run.py` and produce a summary markdown.

## Execution order

```
  Phase 1 (parallel):  A     B     C
                       \     |     /
                        \----+----/
                             |
  Phase 2 (after B):         D
                             |
  Phase 3 (after A,C,D):     E
```

Subagents A, B, C are launched concurrently. Each must write artifacts + a
short `_STATUS.md` so the coordinator can resume.
