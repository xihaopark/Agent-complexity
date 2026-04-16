---
name: finish-tgirke-systempiperdata-chipseq-merge_bams
description: Use this skill when orchestrating the retained "merge_bams" step of the tgirke systempiperdata chipseq finish finish workflow. It keeps the merge bams stage tied to upstream `bam_IGV` and the downstream handoff to `call_peaks_macs_noref`. It tracks completion via `results/finish/merge_bams.done`.
metadata:
  workflow_id: tgirke-systempiperdata-chipseq-finish
  workflow_name: tgirke systempiperdata chipseq finish
  step_id: merge_bams
  step_name: merge bams
---

# Scope
Use this skill only for the `merge_bams` step in `tgirke-systempiperdata-chipseq-finish`.

## Orchestration
- Upstream requirements: `bam_IGV`
- Step file: `finish/tgirke-systempiperdata-chipseq-finish/steps/merge_bams.smk`
- Config file: `finish/tgirke-systempiperdata-chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/merge_bams.done`
- Representative outputs: `results/finish/merge_bams.done`
- Execution targets: `merge_bams`
- Downstream handoff: `call_peaks_macs_noref`

## Guardrails
- Treat `results/finish/merge_bams.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/merge_bams.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `call_peaks_macs_noref` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/merge_bams.done` exists and `call_peaks_macs_noref` can proceed without re-running merge bams.
