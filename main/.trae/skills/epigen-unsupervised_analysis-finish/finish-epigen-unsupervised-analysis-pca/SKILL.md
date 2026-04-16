---
name: finish-epigen-unsupervised-analysis-pca
description: Use this skill when orchestrating the retained "pca" step of the epigen unsupervised_analysis finish finish workflow. It keeps the pca stage tied to upstream `leiden_cluster` and the downstream handoff to `plot_dimred_clustering`. It tracks completion via `results/finish/pca.done`.
metadata:
  workflow_id: epigen-unsupervised_analysis-finish
  workflow_name: epigen unsupervised_analysis finish
  step_id: pca
  step_name: pca
---

# Scope
Use this skill only for the `pca` step in `epigen-unsupervised_analysis-finish`.

## Orchestration
- Upstream requirements: `leiden_cluster`
- Step file: `finish/epigen-unsupervised_analysis-finish/steps/pca.smk`
- Config file: `finish/epigen-unsupervised_analysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/pca.done`
- Representative outputs: `results/finish/pca.done`
- Execution targets: `pca`
- Downstream handoff: `plot_dimred_clustering`

## Guardrails
- Treat `results/finish/pca.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/pca.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plot_dimred_clustering` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/pca.done` exists and `plot_dimred_clustering` can proceed without re-running pca.
