---
name: finish-epigen-unsupervised-analysis-aggregate_clustering_results
description: Use this skill when orchestrating the retained "aggregate_clustering_results" step of the epigen unsupervised_analysis finish finish workflow. It keeps the aggregate clustering results stage tied to upstream `aggregate_all_clustering_results` and the downstream handoff to `aggregate_rank_internal`. It tracks completion via `results/finish/aggregate_clustering_results.done`.
metadata:
  workflow_id: epigen-unsupervised_analysis-finish
  workflow_name: epigen unsupervised_analysis finish
  step_id: aggregate_clustering_results
  step_name: aggregate clustering results
---

# Scope
Use this skill only for the `aggregate_clustering_results` step in `epigen-unsupervised_analysis-finish`.

## Orchestration
- Upstream requirements: `aggregate_all_clustering_results`
- Step file: `finish/epigen-unsupervised_analysis-finish/steps/aggregate_clustering_results.smk`
- Config file: `finish/epigen-unsupervised_analysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/aggregate_clustering_results.done`
- Representative outputs: `results/finish/aggregate_clustering_results.done`
- Execution targets: `aggregate_clustering_results`
- Downstream handoff: `aggregate_rank_internal`

## Guardrails
- Treat `results/finish/aggregate_clustering_results.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/aggregate_clustering_results.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `aggregate_rank_internal` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/aggregate_clustering_results.done` exists and `aggregate_rank_internal` can proceed without re-running aggregate clustering results.
