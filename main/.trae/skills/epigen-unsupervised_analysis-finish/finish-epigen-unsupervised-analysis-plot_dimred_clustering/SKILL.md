---
name: finish-epigen-unsupervised-analysis-plot_dimred_clustering
description: Use this skill when orchestrating the retained "plot_dimred_clustering" step of the epigen unsupervised_analysis finish finish workflow. It keeps the plot dimred clustering stage tied to upstream `pca` and the downstream handoff to `plot_dimred_features`. It tracks completion via `results/finish/plot_dimred_clustering.done`.
metadata:
  workflow_id: epigen-unsupervised_analysis-finish
  workflow_name: epigen unsupervised_analysis finish
  step_id: plot_dimred_clustering
  step_name: plot dimred clustering
---

# Scope
Use this skill only for the `plot_dimred_clustering` step in `epigen-unsupervised_analysis-finish`.

## Orchestration
- Upstream requirements: `pca`
- Step file: `finish/epigen-unsupervised_analysis-finish/steps/plot_dimred_clustering.smk`
- Config file: `finish/epigen-unsupervised_analysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plot_dimred_clustering.done`
- Representative outputs: `results/finish/plot_dimred_clustering.done`
- Execution targets: `plot_dimred_clustering`
- Downstream handoff: `plot_dimred_features`

## Guardrails
- Treat `results/finish/plot_dimred_clustering.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plot_dimred_clustering.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plot_dimred_features` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plot_dimred_clustering.done` exists and `plot_dimred_features` can proceed without re-running plot dimred clustering.
