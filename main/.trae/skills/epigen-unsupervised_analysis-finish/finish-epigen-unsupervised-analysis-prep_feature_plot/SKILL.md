---
name: finish-epigen-unsupervised-analysis-prep_feature_plot
description: Use this skill when orchestrating the retained "prep_feature_plot" step of the epigen unsupervised_analysis finish finish workflow. It keeps the prep feature plot stage tied to upstream `plot_umap_diagnostics` and the downstream handoff to `umap_embed`. It tracks completion via `results/finish/prep_feature_plot.done`.
metadata:
  workflow_id: epigen-unsupervised_analysis-finish
  workflow_name: epigen unsupervised_analysis finish
  step_id: prep_feature_plot
  step_name: prep feature plot
---

# Scope
Use this skill only for the `prep_feature_plot` step in `epigen-unsupervised_analysis-finish`.

## Orchestration
- Upstream requirements: `plot_umap_diagnostics`
- Step file: `finish/epigen-unsupervised_analysis-finish/steps/prep_feature_plot.smk`
- Config file: `finish/epigen-unsupervised_analysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/prep_feature_plot.done`
- Representative outputs: `results/finish/prep_feature_plot.done`
- Execution targets: `prep_feature_plot`
- Downstream handoff: `umap_embed`

## Guardrails
- Treat `results/finish/prep_feature_plot.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/prep_feature_plot.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `umap_embed` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/prep_feature_plot.done` exists and `umap_embed` can proceed without re-running prep feature plot.
