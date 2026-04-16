---
name: finish-joncahn-epigeneticbutton-modkit_summary_dmc
description: Use this skill when orchestrating the retained "modkit_summary_dmc" step of the joncahn epigeneticbutton finish finish workflow. It keeps the modkit summary dmc stage tied to upstream `merge_pileup_sources` and the downstream handoff to `make_mc_stats_dmc`. It tracks completion via `results/finish/modkit_summary_dmc.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: modkit_summary_dmc
  step_name: modkit summary dmc
---

# Scope
Use this skill only for the `modkit_summary_dmc` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `merge_pileup_sources`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/modkit_summary_dmc.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/modkit_summary_dmc.done`
- Representative outputs: `results/finish/modkit_summary_dmc.done`
- Execution targets: `modkit_summary_dmc`
- Downstream handoff: `make_mc_stats_dmc`

## Guardrails
- Treat `results/finish/modkit_summary_dmc.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/modkit_summary_dmc.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `make_mc_stats_dmc` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/modkit_summary_dmc.done` exists and `make_mc_stats_dmc` can proceed without re-running modkit summary dmc.
