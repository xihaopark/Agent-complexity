---
name: finish-maxplanck-ie-snakepipes-plot_heatmap_cov_csaw
description: Use this skill when orchestrating the retained "plot_heatmap_cov_CSAW" step of the maxplanck ie snakepipes finish finish workflow. It keeps the plot heatmap cov CSAW stage tied to upstream `calc_matrix_cov_CSAW` and the downstream handoff to `CSAW_report`. It tracks completion via `results/finish/plot_heatmap_cov_CSAW.done`.
metadata:
  workflow_id: maxplanck-ie-snakepipes-finish
  workflow_name: maxplanck ie snakepipes finish
  step_id: plot_heatmap_cov_CSAW
  step_name: plot heatmap cov CSAW
---

# Scope
Use this skill only for the `plot_heatmap_cov_CSAW` step in `maxplanck-ie-snakepipes-finish`.

## Orchestration
- Upstream requirements: `calc_matrix_cov_CSAW`
- Step file: `finish/maxplanck-ie-snakepipes-finish/steps/plot_heatmap_cov_CSAW.smk`
- Config file: `finish/maxplanck-ie-snakepipes-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plot_heatmap_cov_CSAW.done`
- Representative outputs: `results/finish/plot_heatmap_cov_CSAW.done`
- Execution targets: `plot_heatmap_cov_CSAW`
- Downstream handoff: `CSAW_report`

## Guardrails
- Treat `results/finish/plot_heatmap_cov_CSAW.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plot_heatmap_cov_CSAW.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `CSAW_report` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plot_heatmap_cov_CSAW.done` exists and `CSAW_report` can proceed without re-running plot heatmap cov CSAW.
