---
name: finish-epigen-atacseq-pipeline-peak_calling
description: Use this skill when orchestrating the retained "peak_calling" step of the epigen atacseq_pipeline finish finish workflow. It keeps the peak calling stage tied to upstream `tss_coverage` and the downstream handoff to `aggregate_stats`. It tracks completion via `results/finish/peak_calling.done`.
metadata:
  workflow_id: epigen-atacseq_pipeline-finish
  workflow_name: epigen atacseq_pipeline finish
  step_id: peak_calling
  step_name: peak calling
---

# Scope
Use this skill only for the `peak_calling` step in `epigen-atacseq_pipeline-finish`.

## Orchestration
- Upstream requirements: `tss_coverage`
- Step file: `finish/epigen-atacseq_pipeline-finish/steps/peak_calling.smk`
- Config file: `finish/epigen-atacseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/peak_calling.done`
- Representative outputs: `results/finish/peak_calling.done`
- Execution targets: `peak_calling`
- Downstream handoff: `aggregate_stats`

## Guardrails
- Treat `results/finish/peak_calling.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/peak_calling.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `aggregate_stats` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/peak_calling.done` exists and `aggregate_stats` can proceed without re-running peak calling.
