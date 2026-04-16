---
name: finish-epigen-rnaseq-pipeline-trim_filter
description: Use this skill when orchestrating the retained "trim_filter" step of the epigen rnaseq_pipeline finish finish workflow. It keeps the trim filter stage tied to upstream `check_read_type` and the downstream handoff to `align`. It tracks completion via `results/finish/trim_filter.done`.
metadata:
  workflow_id: epigen-rnaseq_pipeline-finish
  workflow_name: epigen rnaseq_pipeline finish
  step_id: trim_filter
  step_name: trim filter
---

# Scope
Use this skill only for the `trim_filter` step in `epigen-rnaseq_pipeline-finish`.

## Orchestration
- Upstream requirements: `check_read_type`
- Step file: `finish/epigen-rnaseq_pipeline-finish/steps/trim_filter.smk`
- Config file: `finish/epigen-rnaseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/trim_filter.done`
- Representative outputs: `results/finish/trim_filter.done`
- Execution targets: `trim_filter`
- Downstream handoff: `align`

## Guardrails
- Treat `results/finish/trim_filter.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/trim_filter.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `align` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/trim_filter.done` exists and `align` can proceed without re-running trim filter.
