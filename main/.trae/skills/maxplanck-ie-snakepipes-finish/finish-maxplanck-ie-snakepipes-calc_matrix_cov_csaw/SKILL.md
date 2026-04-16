---
name: finish-maxplanck-ie-snakepipes-calc_matrix_cov_csaw
description: Use this skill when orchestrating the retained "calc_matrix_cov_CSAW" step of the maxplanck ie snakepipes finish finish workflow. It keeps the calc matrix cov CSAW stage tied to upstream `plot_heatmap_log2r_CSAW` and the downstream handoff to `plot_heatmap_cov_CSAW`. It tracks completion via `results/finish/calc_matrix_cov_CSAW.done`.
metadata:
  workflow_id: maxplanck-ie-snakepipes-finish
  workflow_name: maxplanck ie snakepipes finish
  step_id: calc_matrix_cov_CSAW
  step_name: calc matrix cov CSAW
---

# Scope
Use this skill only for the `calc_matrix_cov_CSAW` step in `maxplanck-ie-snakepipes-finish`.

## Orchestration
- Upstream requirements: `plot_heatmap_log2r_CSAW`
- Step file: `finish/maxplanck-ie-snakepipes-finish/steps/calc_matrix_cov_CSAW.smk`
- Config file: `finish/maxplanck-ie-snakepipes-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/calc_matrix_cov_CSAW.done`
- Representative outputs: `results/finish/calc_matrix_cov_CSAW.done`
- Execution targets: `calc_matrix_cov_CSAW`
- Downstream handoff: `plot_heatmap_cov_CSAW`

## Guardrails
- Treat `results/finish/calc_matrix_cov_CSAW.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/calc_matrix_cov_CSAW.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plot_heatmap_cov_CSAW` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/calc_matrix_cov_CSAW.done` exists and `plot_heatmap_cov_CSAW` can proceed without re-running calc matrix cov CSAW.
