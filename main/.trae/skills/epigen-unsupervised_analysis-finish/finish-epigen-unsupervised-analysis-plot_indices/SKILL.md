---
name: finish-epigen-unsupervised-analysis-plot_indices
description: Use this skill when orchestrating the retained "plot_indices" step of the epigen unsupervised_analysis finish finish workflow. It keeps the plot indices stage tied to upstream `plot_heatmap` and the downstream handoff to `plot_pca_diagnostics`. It tracks completion via `results/finish/plot_indices.done`.
metadata:
  workflow_id: epigen-unsupervised_analysis-finish
  workflow_name: epigen unsupervised_analysis finish
  step_id: plot_indices
  step_name: plot indices
---

# Scope
Use this skill only for the `plot_indices` step in `epigen-unsupervised_analysis-finish`.

## Orchestration
- Upstream requirements: `plot_heatmap`
- Step file: `finish/epigen-unsupervised_analysis-finish/steps/plot_indices.smk`
- Config file: `finish/epigen-unsupervised_analysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plot_indices.done`
- Representative outputs: `results/finish/plot_indices.done`
- Execution targets: `plot_indices`
- Downstream handoff: `plot_pca_diagnostics`

## Guardrails
- Treat `results/finish/plot_indices.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plot_indices.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plot_pca_diagnostics` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plot_indices.done` exists and `plot_pca_diagnostics` can proceed without re-running plot indices.
