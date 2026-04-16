---
name: finish-epigen-unsupervised-analysis-plot_pca_diagnostics
description: Use this skill when orchestrating the retained "plot_pca_diagnostics" step of the epigen unsupervised_analysis finish finish workflow. It keeps the plot pca diagnostics stage tied to upstream `plot_indices` and the downstream handoff to `plot_umap_connectivity`. It tracks completion via `results/finish/plot_pca_diagnostics.done`.
metadata:
  workflow_id: epigen-unsupervised_analysis-finish
  workflow_name: epigen unsupervised_analysis finish
  step_id: plot_pca_diagnostics
  step_name: plot pca diagnostics
---

# Scope
Use this skill only for the `plot_pca_diagnostics` step in `epigen-unsupervised_analysis-finish`.

## Orchestration
- Upstream requirements: `plot_indices`
- Step file: `finish/epigen-unsupervised_analysis-finish/steps/plot_pca_diagnostics.smk`
- Config file: `finish/epigen-unsupervised_analysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plot_pca_diagnostics.done`
- Representative outputs: `results/finish/plot_pca_diagnostics.done`
- Execution targets: `plot_pca_diagnostics`
- Downstream handoff: `plot_umap_connectivity`

## Guardrails
- Treat `results/finish/plot_pca_diagnostics.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plot_pca_diagnostics.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plot_umap_connectivity` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plot_pca_diagnostics.done` exists and `plot_umap_connectivity` can proceed without re-running plot pca diagnostics.
