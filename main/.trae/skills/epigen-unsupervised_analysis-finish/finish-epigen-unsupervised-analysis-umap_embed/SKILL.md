---
name: finish-epigen-unsupervised-analysis-umap_embed
description: Use this skill when orchestrating the retained "umap_embed" step of the epigen unsupervised_analysis finish finish workflow. It keeps the umap embed stage tied to upstream `prep_feature_plot` and the downstream handoff to `umap_graph`. It tracks completion via `results/finish/umap_embed.done`.
metadata:
  workflow_id: epigen-unsupervised_analysis-finish
  workflow_name: epigen unsupervised_analysis finish
  step_id: umap_embed
  step_name: umap embed
---

# Scope
Use this skill only for the `umap_embed` step in `epigen-unsupervised_analysis-finish`.

## Orchestration
- Upstream requirements: `prep_feature_plot`
- Step file: `finish/epigen-unsupervised_analysis-finish/steps/umap_embed.smk`
- Config file: `finish/epigen-unsupervised_analysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/umap_embed.done`
- Representative outputs: `results/finish/umap_embed.done`
- Execution targets: `umap_embed`
- Downstream handoff: `umap_graph`

## Guardrails
- Treat `results/finish/umap_embed.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/umap_embed.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `umap_graph` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/umap_embed.done` exists and `umap_graph` can proceed without re-running umap embed.
