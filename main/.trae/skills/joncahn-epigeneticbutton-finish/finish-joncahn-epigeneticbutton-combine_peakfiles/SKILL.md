---
name: finish-joncahn-epigeneticbutton-combine_peakfiles
description: Use this skill when orchestrating the retained "combine_peakfiles" step of the joncahn epigeneticbutton finish finish workflow. It keeps the combine peakfiles stage tied to upstream `combine_clusterfiles` and the downstream handoff to `combine_TSS`. It tracks completion via `results/finish/combine_peakfiles.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: combine_peakfiles
  step_name: combine peakfiles
---

# Scope
Use this skill only for the `combine_peakfiles` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `combine_clusterfiles`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/combine_peakfiles.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/combine_peakfiles.done`
- Representative outputs: `results/finish/combine_peakfiles.done`
- Execution targets: `combine_peakfiles`
- Downstream handoff: `combine_TSS`

## Guardrails
- Treat `results/finish/combine_peakfiles.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/combine_peakfiles.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `combine_TSS` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/combine_peakfiles.done` exists and `combine_TSS` can proceed without re-running combine peakfiles.
