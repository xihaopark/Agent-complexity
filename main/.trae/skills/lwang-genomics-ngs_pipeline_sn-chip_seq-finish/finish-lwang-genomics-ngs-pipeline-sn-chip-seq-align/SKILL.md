---
name: finish-lwang-genomics-ngs-pipeline-sn-chip-seq-align
description: Use this skill when orchestrating the retained "align" step of the lwang genomics ngs_pipeline_sn chip_seq finish finish workflow. It keeps the align stage tied to upstream `trim` and the downstream handoff to `filter_sort_index`. It tracks completion via `results/finish/align.done`.
metadata:
  workflow_id: lwang-genomics-ngs_pipeline_sn-chip_seq-finish
  workflow_name: lwang genomics ngs_pipeline_sn chip_seq finish
  step_id: align
  step_name: align
---

# Scope
Use this skill only for the `align` step in `lwang-genomics-ngs_pipeline_sn-chip_seq-finish`.

## Orchestration
- Upstream requirements: `trim`
- Step file: `finish/lwang-genomics-ngs_pipeline_sn-chip_seq-finish/steps/align.smk`
- Config file: `finish/lwang-genomics-ngs_pipeline_sn-chip_seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/align.done`
- Representative outputs: `results/finish/align.done`
- Execution targets: `align`
- Downstream handoff: `filter_sort_index`

## Guardrails
- Treat `results/finish/align.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/align.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `filter_sort_index` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/align.done` exists and `filter_sort_index` can proceed without re-running align.
