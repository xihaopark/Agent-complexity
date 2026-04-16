---
name: finish-joncahn-epigeneticbutton-combine_clusterfiles
description: Use this skill when orchestrating the retained "combine_clusterfiles" step of the joncahn epigeneticbutton finish finish workflow. It keeps the combine clusterfiles stage tied to upstream `plotting_srna_sizes_stats` and the downstream handoff to `combine_peakfiles`. It tracks completion via `results/finish/combine_clusterfiles.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: combine_clusterfiles
  step_name: combine clusterfiles
---

# Scope
Use this skill only for the `combine_clusterfiles` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `plotting_srna_sizes_stats`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/combine_clusterfiles.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/combine_clusterfiles.done`
- Representative outputs: `results/finish/combine_clusterfiles.done`
- Execution targets: `combine_clusterfiles`
- Downstream handoff: `combine_peakfiles`

## Guardrails
- Treat `results/finish/combine_clusterfiles.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/combine_clusterfiles.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `combine_peakfiles` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/combine_clusterfiles.done` exists and `combine_peakfiles` can proceed without re-running combine clusterfiles.
