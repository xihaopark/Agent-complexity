---
name: finish-joncahn-epigeneticbutton-make_mc_stats_pe
description: Use this skill when orchestrating the retained "make_mc_stats_pe" step of the joncahn epigeneticbutton finish finish workflow. It keeps the make mc stats pe stage tied to upstream `pe_or_se_mc_dispatch` and the downstream handoff to `make_mc_stats_se`. It tracks completion via `results/finish/make_mc_stats_pe.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: make_mc_stats_pe
  step_name: make mc stats pe
---

# Scope
Use this skill only for the `make_mc_stats_pe` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `pe_or_se_mc_dispatch`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/make_mc_stats_pe.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/make_mc_stats_pe.done`
- Representative outputs: `results/finish/make_mc_stats_pe.done`
- Execution targets: `make_mc_stats_pe`
- Downstream handoff: `make_mc_stats_se`

## Guardrails
- Treat `results/finish/make_mc_stats_pe.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/make_mc_stats_pe.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `make_mc_stats_se` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/make_mc_stats_pe.done` exists and `make_mc_stats_se` can proceed without re-running make mc stats pe.
