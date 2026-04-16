---
name: finish-snakemake-workflows-chipseq-mark_merged_duplicates
description: Use this skill when orchestrating the retained "mark_merged_duplicates" step of the snakemake workflows chipseq finish finish workflow. It keeps the mark merged duplicates stage tied to upstream `merge_bams` and the downstream handoff to `samtools_view_filter`. It tracks completion via `results/finish/mark_merged_duplicates.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: mark_merged_duplicates
  step_name: mark merged duplicates
---

# Scope
Use this skill only for the `mark_merged_duplicates` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `merge_bams`
- Step file: `finish/chipseq-finish/steps/mark_merged_duplicates.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/mark_merged_duplicates.done`
- Representative outputs: `results/finish/mark_merged_duplicates.done`
- Execution targets: `mark_merged_duplicates`
- Downstream handoff: `samtools_view_filter`

## Guardrails
- Treat `results/finish/mark_merged_duplicates.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/mark_merged_duplicates.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `samtools_view_filter` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/mark_merged_duplicates.done` exists and `samtools_view_filter` can proceed without re-running mark merged duplicates.
