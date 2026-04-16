---
name: finish-tgirke-systempiperdata-chipseq-bam_igv
description: Use this skill when orchestrating the retained "bam_IGV" step of the tgirke systempiperdata chipseq finish finish workflow. It keeps the bam IGV stage tied to upstream `align_stats` and the downstream handoff to `merge_bams`. It tracks completion via `results/finish/bam_IGV.done`.
metadata:
  workflow_id: tgirke-systempiperdata-chipseq-finish
  workflow_name: tgirke systempiperdata chipseq finish
  step_id: bam_IGV
  step_name: bam IGV
---

# Scope
Use this skill only for the `bam_IGV` step in `tgirke-systempiperdata-chipseq-finish`.

## Orchestration
- Upstream requirements: `align_stats`
- Step file: `finish/tgirke-systempiperdata-chipseq-finish/steps/bam_IGV.smk`
- Config file: `finish/tgirke-systempiperdata-chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/bam_IGV.done`
- Representative outputs: `results/finish/bam_IGV.done`
- Execution targets: `bam_IGV`
- Downstream handoff: `merge_bams`

## Guardrails
- Treat `results/finish/bam_IGV.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/bam_IGV.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `merge_bams` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/bam_IGV.done` exists and `merge_bams` can proceed without re-running bam IGV.
