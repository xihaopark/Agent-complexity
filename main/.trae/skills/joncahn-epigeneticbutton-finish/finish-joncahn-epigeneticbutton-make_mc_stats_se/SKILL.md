---
name: finish-joncahn-epigeneticbutton-make_mc_stats_se
description: Use this skill when orchestrating the retained "make_mc_stats_se" step of the joncahn epigeneticbutton finish finish workflow. It keeps the make mc stats se stage tied to upstream `make_mc_stats_pe` and the downstream handoff to `merging_mc_replicates`. It tracks completion via `results/finish/make_mc_stats_se.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: make_mc_stats_se
  step_name: make mc stats se
---

# Scope
Use this skill only for the `make_mc_stats_se` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `make_mc_stats_pe`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/make_mc_stats_se.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/make_mc_stats_se.done`
- Representative outputs: `results/finish/make_mc_stats_se.done`
- Execution targets: `make_mc_stats_se`
- Downstream handoff: `merging_mc_replicates`

## Guardrails
- Treat `results/finish/make_mc_stats_se.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/make_mc_stats_se.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `merging_mc_replicates` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/make_mc_stats_se.done` exists and `merging_mc_replicates` can proceed without re-running make mc stats se.
