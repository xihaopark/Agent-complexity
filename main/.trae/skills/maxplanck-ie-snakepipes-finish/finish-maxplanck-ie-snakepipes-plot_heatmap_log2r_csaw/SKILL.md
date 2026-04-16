---
name: finish-maxplanck-ie-snakepipes-plot_heatmap_log2r_csaw
description: Use this skill when orchestrating the retained "plot_heatmap_log2r_CSAW" step of the maxplanck ie snakepipes finish finish workflow. It keeps the plot heatmap log2r CSAW stage tied to upstream `calc_matrix_log2r_CSAW` and the downstream handoff to `calc_matrix_cov_CSAW`. It tracks completion via `results/finish/plot_heatmap_log2r_CSAW.done`.
metadata:
  workflow_id: maxplanck-ie-snakepipes-finish
  workflow_name: maxplanck ie snakepipes finish
  step_id: plot_heatmap_log2r_CSAW
  step_name: plot heatmap log2r CSAW
---

# Scope
Use this skill only for the `plot_heatmap_log2r_CSAW` step in `maxplanck-ie-snakepipes-finish`.

## Orchestration
- Upstream requirements: `calc_matrix_log2r_CSAW`
- Step file: `finish/maxplanck-ie-snakepipes-finish/steps/plot_heatmap_log2r_CSAW.smk`
- Config file: `finish/maxplanck-ie-snakepipes-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plot_heatmap_log2r_CSAW.done`
- Representative outputs: `results/finish/plot_heatmap_log2r_CSAW.done`
- Execution targets: `plot_heatmap_log2r_CSAW`
- Downstream handoff: `calc_matrix_cov_CSAW`

## Guardrails
- Treat `results/finish/plot_heatmap_log2r_CSAW.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plot_heatmap_log2r_CSAW.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `calc_matrix_cov_CSAW` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plot_heatmap_log2r_CSAW.done` exists and `calc_matrix_cov_CSAW` can proceed without re-running plot heatmap log2r CSAW.
