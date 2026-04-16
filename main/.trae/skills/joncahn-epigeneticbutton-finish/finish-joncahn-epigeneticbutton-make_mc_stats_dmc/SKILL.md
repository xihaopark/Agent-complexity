---
name: finish-joncahn-epigeneticbutton-make_mc_stats_dmc
description: Use this skill when orchestrating the retained "make_mc_stats_dmc" step of the joncahn epigeneticbutton finish finish workflow. It keeps the make mc stats dmc stage tied to upstream `modkit_summary_dmc` and the downstream handoff to `convert_bedmethyl_to_cx_report`. It tracks completion via `results/finish/make_mc_stats_dmc.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: make_mc_stats_dmc
  step_name: make mc stats dmc
---

# Scope
Use this skill only for the `make_mc_stats_dmc` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `modkit_summary_dmc`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/make_mc_stats_dmc.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/make_mc_stats_dmc.done`
- Representative outputs: `results/finish/make_mc_stats_dmc.done`
- Execution targets: `make_mc_stats_dmc`
- Downstream handoff: `convert_bedmethyl_to_cx_report`

## Guardrails
- Treat `results/finish/make_mc_stats_dmc.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/make_mc_stats_dmc.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `convert_bedmethyl_to_cx_report` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/make_mc_stats_dmc.done` exists and `convert_bedmethyl_to_cx_report` can proceed without re-running make mc stats dmc.
