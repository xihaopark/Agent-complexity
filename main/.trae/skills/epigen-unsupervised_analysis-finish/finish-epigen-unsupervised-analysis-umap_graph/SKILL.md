---
name: finish-epigen-unsupervised-analysis-umap_graph
description: Use this skill when orchestrating the retained "umap_graph" step of the epigen unsupervised_analysis finish finish workflow. It keeps the umap graph stage tied to upstream `umap_embed` and the downstream handoff to `validation_external`. It tracks completion via `results/finish/umap_graph.done`.
metadata:
  workflow_id: epigen-unsupervised_analysis-finish
  workflow_name: epigen unsupervised_analysis finish
  step_id: umap_graph
  step_name: umap graph
---

# Scope
Use this skill only for the `umap_graph` step in `epigen-unsupervised_analysis-finish`.

## Orchestration
- Upstream requirements: `umap_embed`
- Step file: `finish/epigen-unsupervised_analysis-finish/steps/umap_graph.smk`
- Config file: `finish/epigen-unsupervised_analysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/umap_graph.done`
- Representative outputs: `results/finish/umap_graph.done`
- Execution targets: `umap_graph`
- Downstream handoff: `validation_external`

## Guardrails
- Treat `results/finish/umap_graph.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/umap_graph.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `validation_external` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/umap_graph.done` exists and `validation_external` can proceed without re-running umap graph.
