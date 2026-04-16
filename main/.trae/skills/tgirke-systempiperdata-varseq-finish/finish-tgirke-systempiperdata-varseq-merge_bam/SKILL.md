---
name: finish-tgirke-systempiperdata-varseq-merge_bam
description: Use this skill when orchestrating the retained "merge_bam" step of the tgirke systempiperdata varseq finish finish workflow. It keeps the merge bam stage tied to upstream `fastq2ubam` and the downstream handoff to `sort`. It tracks completion via `results/finish/merge_bam.done`.
metadata:
  workflow_id: tgirke-systempiperdata-varseq-finish
  workflow_name: tgirke systempiperdata varseq finish
  step_id: merge_bam
  step_name: merge bam
---

# Scope
Use this skill only for the `merge_bam` step in `tgirke-systempiperdata-varseq-finish`.

## Orchestration
- Upstream requirements: `fastq2ubam`
- Step file: `finish/tgirke-systempiperdata-varseq-finish/steps/merge_bam.smk`
- Config file: `finish/tgirke-systempiperdata-varseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/merge_bam.done`
- Representative outputs: `results/finish/merge_bam.done`
- Execution targets: `merge_bam`
- Downstream handoff: `sort`

## Guardrails
- Treat `results/finish/merge_bam.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/merge_bam.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `sort` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/merge_bam.done` exists and `sort` can proceed without re-running merge bam.
