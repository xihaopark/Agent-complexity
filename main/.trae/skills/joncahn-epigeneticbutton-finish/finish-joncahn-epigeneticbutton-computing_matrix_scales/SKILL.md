---
name: finish-joncahn-epigeneticbutton-computing_matrix_scales
description: Use this skill when orchestrating the retained "computing_matrix_scales" step of the joncahn epigeneticbutton finish finish workflow. It keeps the computing matrix scales stage tied to upstream `merging_matrix` and the downstream handoff to `plotting_heatmap_on_targetfile`. It tracks completion via `results/finish/computing_matrix_scales.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: computing_matrix_scales
  step_name: computing matrix scales
---

# Scope
Use this skill only for the `computing_matrix_scales` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `merging_matrix`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/computing_matrix_scales.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/computing_matrix_scales.done`
- Representative outputs: `results/finish/computing_matrix_scales.done`
- Execution targets: `computing_matrix_scales`
- Downstream handoff: `plotting_heatmap_on_targetfile`

## Guardrails
- Treat `results/finish/computing_matrix_scales.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/computing_matrix_scales.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plotting_heatmap_on_targetfile` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/computing_matrix_scales.done` exists and `plotting_heatmap_on_targetfile` can proceed without re-running computing matrix scales.
