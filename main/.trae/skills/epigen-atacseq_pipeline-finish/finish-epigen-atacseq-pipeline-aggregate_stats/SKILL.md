---
name: finish-epigen-atacseq-pipeline-aggregate_stats
description: Use this skill when orchestrating the retained "aggregate_stats" step of the epigen atacseq_pipeline finish finish workflow. It keeps the aggregate stats stage tied to upstream `peak_calling` and the downstream handoff to `symlink_stats`. It tracks completion via `results/finish/aggregate_stats.done`.
metadata:
  workflow_id: epigen-atacseq_pipeline-finish
  workflow_name: epigen atacseq_pipeline finish
  step_id: aggregate_stats
  step_name: aggregate stats
---

# Scope
Use this skill only for the `aggregate_stats` step in `epigen-atacseq_pipeline-finish`.

## Orchestration
- Upstream requirements: `peak_calling`
- Step file: `finish/epigen-atacseq_pipeline-finish/steps/aggregate_stats.smk`
- Config file: `finish/epigen-atacseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/aggregate_stats.done`
- Representative outputs: `results/finish/aggregate_stats.done`
- Execution targets: `aggregate_stats`
- Downstream handoff: `symlink_stats`

## Guardrails
- Treat `results/finish/aggregate_stats.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/aggregate_stats.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `symlink_stats` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/aggregate_stats.done` exists and `symlink_stats` can proceed without re-running aggregate stats.
