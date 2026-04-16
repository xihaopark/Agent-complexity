---
name: finish-epigen-unsupervised-analysis-plot_umap_connectivity
description: Use this skill when orchestrating the retained "plot_umap_connectivity" step of the epigen unsupervised_analysis finish finish workflow. It keeps the plot umap connectivity stage tied to upstream `plot_pca_diagnostics` and the downstream handoff to `plot_umap_diagnostics`. It tracks completion via `results/finish/plot_umap_connectivity.done`.
metadata:
  workflow_id: epigen-unsupervised_analysis-finish
  workflow_name: epigen unsupervised_analysis finish
  step_id: plot_umap_connectivity
  step_name: plot umap connectivity
---

# Scope
Use this skill only for the `plot_umap_connectivity` step in `epigen-unsupervised_analysis-finish`.

## Orchestration
- Upstream requirements: `plot_pca_diagnostics`
- Step file: `finish/epigen-unsupervised_analysis-finish/steps/plot_umap_connectivity.smk`
- Config file: `finish/epigen-unsupervised_analysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plot_umap_connectivity.done`
- Representative outputs: `results/finish/plot_umap_connectivity.done`
- Execution targets: `plot_umap_connectivity`
- Downstream handoff: `plot_umap_diagnostics`

## Guardrails
- Treat `results/finish/plot_umap_connectivity.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plot_umap_connectivity.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plot_umap_diagnostics` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plot_umap_connectivity.done` exists and `plot_umap_diagnostics` can proceed without re-running plot umap connectivity.
