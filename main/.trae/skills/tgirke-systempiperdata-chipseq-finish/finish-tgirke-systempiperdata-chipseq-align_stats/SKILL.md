---
name: finish-tgirke-systempiperdata-chipseq-align_stats
description: Use this skill when orchestrating the retained "align_stats" step of the tgirke systempiperdata chipseq finish finish workflow. It keeps the align stats stage tied to upstream `bowtie2_alignment` and the downstream handoff to `bam_IGV`. It tracks completion via `results/finish/align_stats.done`.
metadata:
  workflow_id: tgirke-systempiperdata-chipseq-finish
  workflow_name: tgirke systempiperdata chipseq finish
  step_id: align_stats
  step_name: align stats
---

# Scope
Use this skill only for the `align_stats` step in `tgirke-systempiperdata-chipseq-finish`.

## Orchestration
- Upstream requirements: `bowtie2_alignment`
- Step file: `finish/tgirke-systempiperdata-chipseq-finish/steps/align_stats.smk`
- Config file: `finish/tgirke-systempiperdata-chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/align_stats.done`
- Representative outputs: `results/finish/align_stats.done`
- Execution targets: `align_stats`
- Downstream handoff: `bam_IGV`

## Guardrails
- Treat `results/finish/align_stats.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/align_stats.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `bam_IGV` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/align_stats.done` exists and `bam_IGV` can proceed without re-running align stats.
