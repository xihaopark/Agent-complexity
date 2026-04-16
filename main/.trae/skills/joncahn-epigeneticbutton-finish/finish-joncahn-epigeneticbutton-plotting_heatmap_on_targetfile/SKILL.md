---
name: finish-joncahn-epigeneticbutton-plotting_heatmap_on_targetfile
description: Use this skill when orchestrating the retained "plotting_heatmap_on_targetfile" step of the joncahn epigeneticbutton finish finish workflow. It keeps the plotting heatmap on targetfile stage tied to upstream `computing_matrix_scales` and the downstream handoff to `sort_heatmap`. It tracks completion via `results/finish/plotting_heatmap_on_targetfile.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: plotting_heatmap_on_targetfile
  step_name: plotting heatmap on targetfile
---

# Scope
Use this skill only for the `plotting_heatmap_on_targetfile` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `computing_matrix_scales`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/plotting_heatmap_on_targetfile.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plotting_heatmap_on_targetfile.done`
- Representative outputs: `results/finish/plotting_heatmap_on_targetfile.done`
- Execution targets: `plotting_heatmap_on_targetfile`
- Downstream handoff: `sort_heatmap`

## Guardrails
- Treat `results/finish/plotting_heatmap_on_targetfile.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plotting_heatmap_on_targetfile.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `sort_heatmap` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plotting_heatmap_on_targetfile.done` exists and `sort_heatmap` can proceed without re-running plotting heatmap on targetfile.
