---
name: finish-snakemake-workflows-chipseq-merge_bams
description: Use this skill when orchestrating the retained "merge_bams" step of the snakemake workflows chipseq finish finish workflow. It keeps the merge bams stage tied to upstream `bwa_mem` and the downstream handoff to `mark_merged_duplicates`. It tracks completion via `results/finish/merge_bams.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: merge_bams
  step_name: merge bams
---

# Scope
Use this skill only for the `merge_bams` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `bwa_mem`
- Step file: `finish/chipseq-finish/steps/merge_bams.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/merge_bams.done`
- Representative outputs: `results/finish/merge_bams.done`
- Execution targets: `merge_bams`
- Downstream handoff: `mark_merged_duplicates`

## Guardrails
- Treat `results/finish/merge_bams.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/merge_bams.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `mark_merged_duplicates` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/merge_bams.done` exists and `mark_merged_duplicates` can proceed without re-running merge bams.
