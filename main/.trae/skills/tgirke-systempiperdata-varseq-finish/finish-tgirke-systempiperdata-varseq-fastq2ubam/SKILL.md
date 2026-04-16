---
name: finish-tgirke-systempiperdata-varseq-fastq2ubam
description: Use this skill when orchestrating the retained "fastq2ubam" step of the tgirke systempiperdata varseq finish finish workflow. It keeps the fastq2ubam stage tied to upstream `bam_urls` and the downstream handoff to `merge_bam`. It tracks completion via `results/finish/fastq2ubam.done`.
metadata:
  workflow_id: tgirke-systempiperdata-varseq-finish
  workflow_name: tgirke systempiperdata varseq finish
  step_id: fastq2ubam
  step_name: fastq2ubam
---

# Scope
Use this skill only for the `fastq2ubam` step in `tgirke-systempiperdata-varseq-finish`.

## Orchestration
- Upstream requirements: `bam_urls`
- Step file: `finish/tgirke-systempiperdata-varseq-finish/steps/fastq2ubam.smk`
- Config file: `finish/tgirke-systempiperdata-varseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/fastq2ubam.done`
- Representative outputs: `results/finish/fastq2ubam.done`
- Execution targets: `fastq2ubam`
- Downstream handoff: `merge_bam`

## Guardrails
- Treat `results/finish/fastq2ubam.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/fastq2ubam.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `merge_bam` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/fastq2ubam.done` exists and `merge_bam` can proceed without re-running fastq2ubam.
