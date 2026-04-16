---
name: finish-epigen-unsupervised-analysis-distance_matrix
description: Use this skill when orchestrating the retained "distance_matrix" step of the epigen unsupervised_analysis finish finish workflow. It keeps the distance matrix stage tied to upstream `densmap_embed` and the downstream handoff to `env_export`. It tracks completion via `results/finish/distance_matrix.done`.
metadata:
  workflow_id: epigen-unsupervised_analysis-finish
  workflow_name: epigen unsupervised_analysis finish
  step_id: distance_matrix
  step_name: distance matrix
---

# Scope
Use this skill only for the `distance_matrix` step in `epigen-unsupervised_analysis-finish`.

## Orchestration
- Upstream requirements: `densmap_embed`
- Step file: `finish/epigen-unsupervised_analysis-finish/steps/distance_matrix.smk`
- Config file: `finish/epigen-unsupervised_analysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/distance_matrix.done`
- Representative outputs: `results/finish/distance_matrix.done`
- Execution targets: `distance_matrix`
- Downstream handoff: `env_export`

## Guardrails
- Treat `results/finish/distance_matrix.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/distance_matrix.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `env_export` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/distance_matrix.done` exists and `env_export` can proceed without re-running distance matrix.
