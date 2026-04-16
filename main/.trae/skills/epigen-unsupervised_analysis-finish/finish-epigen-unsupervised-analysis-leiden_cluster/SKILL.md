---
name: finish-epigen-unsupervised-analysis-leiden_cluster
description: Use this skill when orchestrating the retained "leiden_cluster" step of the epigen unsupervised_analysis finish finish workflow. It keeps the leiden cluster stage tied to upstream `env_export` and the downstream handoff to `pca`. It tracks completion via `results/finish/leiden_cluster.done`.
metadata:
  workflow_id: epigen-unsupervised_analysis-finish
  workflow_name: epigen unsupervised_analysis finish
  step_id: leiden_cluster
  step_name: leiden cluster
---

# Scope
Use this skill only for the `leiden_cluster` step in `epigen-unsupervised_analysis-finish`.

## Orchestration
- Upstream requirements: `env_export`
- Step file: `finish/epigen-unsupervised_analysis-finish/steps/leiden_cluster.smk`
- Config file: `finish/epigen-unsupervised_analysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/leiden_cluster.done`
- Representative outputs: `results/finish/leiden_cluster.done`
- Execution targets: `leiden_cluster`
- Downstream handoff: `pca`

## Guardrails
- Treat `results/finish/leiden_cluster.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/leiden_cluster.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `pca` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/leiden_cluster.done` exists and `pca` can proceed without re-running leiden cluster.
