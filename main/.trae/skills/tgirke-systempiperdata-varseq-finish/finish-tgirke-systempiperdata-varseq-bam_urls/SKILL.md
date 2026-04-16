---
name: finish-tgirke-systempiperdata-varseq-bam_urls
description: Use this skill when orchestrating the retained "bam_urls" step of the tgirke systempiperdata varseq finish finish workflow. It keeps the bam urls stage tied to upstream `align_stats` and the downstream handoff to `fastq2ubam`. It tracks completion via `results/finish/bam_urls.done`.
metadata:
  workflow_id: tgirke-systempiperdata-varseq-finish
  workflow_name: tgirke systempiperdata varseq finish
  step_id: bam_urls
  step_name: bam urls
---

# Scope
Use this skill only for the `bam_urls` step in `tgirke-systempiperdata-varseq-finish`.

## Orchestration
- Upstream requirements: `align_stats`
- Step file: `finish/tgirke-systempiperdata-varseq-finish/steps/bam_urls.smk`
- Config file: `finish/tgirke-systempiperdata-varseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/bam_urls.done`
- Representative outputs: `results/finish/bam_urls.done`
- Execution targets: `bam_urls`
- Downstream handoff: `fastq2ubam`

## Guardrails
- Treat `results/finish/bam_urls.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/bam_urls.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `fastq2ubam` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/bam_urls.done` exists and `fastq2ubam` can proceed without re-running bam urls.
