---
name: finish-epigen-unsupervised-analysis-aggregate_all_clustering_results
description: Use this skill when orchestrating the retained "aggregate_all_clustering_results" step of the epigen unsupervised_analysis finish finish workflow. It keeps the aggregate all clustering results stage and the downstream handoff to `aggregate_clustering_results`. It tracks completion via `results/finish/aggregate_all_clustering_results.done`.
metadata:
  workflow_id: epigen-unsupervised_analysis-finish
  workflow_name: epigen unsupervised_analysis finish
  step_id: aggregate_all_clustering_results
  step_name: aggregate all clustering results
---

# Scope
Use this skill only for the `aggregate_all_clustering_results` step in `epigen-unsupervised_analysis-finish`.

## Orchestration
- Upstream requirements: none
- Step file: `finish/epigen-unsupervised_analysis-finish/steps/aggregate_all_clustering_results.smk`
- Config file: `finish/epigen-unsupervised_analysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/aggregate_all_clustering_results.done`
- Representative outputs: `results/finish/aggregate_all_clustering_results.done`
- Execution targets: `aggregate_all_clustering_results`
- Downstream handoff: `aggregate_clustering_results`

## Guardrails
- Treat `results/finish/aggregate_all_clustering_results.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/aggregate_all_clustering_results.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `aggregate_clustering_results` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/aggregate_all_clustering_results.done` exists and `aggregate_clustering_results` can proceed without re-running aggregate all clustering results.
