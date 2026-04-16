---
name: finish-epigen-unsupervised-analysis-aggregate_rank_internal
description: Use this skill when orchestrating the retained "aggregate_rank_internal" step of the epigen unsupervised_analysis finish finish workflow. It keeps the aggregate rank internal stage tied to upstream `aggregate_clustering_results` and the downstream handoff to `annot_export`. It tracks completion via `results/finish/aggregate_rank_internal.done`.
metadata:
  workflow_id: epigen-unsupervised_analysis-finish
  workflow_name: epigen unsupervised_analysis finish
  step_id: aggregate_rank_internal
  step_name: aggregate rank internal
---

# Scope
Use this skill only for the `aggregate_rank_internal` step in `epigen-unsupervised_analysis-finish`.

## Orchestration
- Upstream requirements: `aggregate_clustering_results`
- Step file: `finish/epigen-unsupervised_analysis-finish/steps/aggregate_rank_internal.smk`
- Config file: `finish/epigen-unsupervised_analysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/aggregate_rank_internal.done`
- Representative outputs: `results/finish/aggregate_rank_internal.done`
- Execution targets: `aggregate_rank_internal`
- Downstream handoff: `annot_export`

## Guardrails
- Treat `results/finish/aggregate_rank_internal.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/aggregate_rank_internal.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `annot_export` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/aggregate_rank_internal.done` exists and `annot_export` can proceed without re-running aggregate rank internal.
