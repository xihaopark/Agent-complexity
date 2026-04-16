---
name: finish-epigen-unsupervised-analysis-plot_umap_diagnostics
description: Use this skill when orchestrating the retained "plot_umap_diagnostics" step of the epigen unsupervised_analysis finish finish workflow. It keeps the plot umap diagnostics stage tied to upstream `plot_umap_connectivity` and the downstream handoff to `prep_feature_plot`. It tracks completion via `results/finish/plot_umap_diagnostics.done`.
metadata:
  workflow_id: epigen-unsupervised_analysis-finish
  workflow_name: epigen unsupervised_analysis finish
  step_id: plot_umap_diagnostics
  step_name: plot umap diagnostics
---

# Scope
Use this skill only for the `plot_umap_diagnostics` step in `epigen-unsupervised_analysis-finish`.

## Orchestration
- Upstream requirements: `plot_umap_connectivity`
- Step file: `finish/epigen-unsupervised_analysis-finish/steps/plot_umap_diagnostics.smk`
- Config file: `finish/epigen-unsupervised_analysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plot_umap_diagnostics.done`
- Representative outputs: `results/finish/plot_umap_diagnostics.done`
- Execution targets: `plot_umap_diagnostics`
- Downstream handoff: `prep_feature_plot`

## Guardrails
- Treat `results/finish/plot_umap_diagnostics.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plot_umap_diagnostics.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `prep_feature_plot` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plot_umap_diagnostics.done` exists and `prep_feature_plot` can proceed without re-running plot umap diagnostics.
