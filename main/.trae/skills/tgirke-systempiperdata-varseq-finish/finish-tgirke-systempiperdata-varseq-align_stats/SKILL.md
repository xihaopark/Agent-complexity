---
name: finish-tgirke-systempiperdata-varseq-align_stats
description: Use this skill when orchestrating the retained "align_stats" step of the tgirke systempiperdata varseq finish finish workflow. It keeps the align stats stage tied to upstream `bwa_alignment` and the downstream handoff to `bam_urls`. It tracks completion via `results/finish/align_stats.done`.
metadata:
  workflow_id: tgirke-systempiperdata-varseq-finish
  workflow_name: tgirke systempiperdata varseq finish
  step_id: align_stats
  step_name: align stats
---

# Scope
Use this skill only for the `align_stats` step in `tgirke-systempiperdata-varseq-finish`.

## Orchestration
- Upstream requirements: `bwa_alignment`
- Step file: `finish/tgirke-systempiperdata-varseq-finish/steps/align_stats.smk`
- Config file: `finish/tgirke-systempiperdata-varseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/align_stats.done`
- Representative outputs: `results/finish/align_stats.done`
- Execution targets: `align_stats`
- Downstream handoff: `bam_urls`

## Guardrails
- Treat `results/finish/align_stats.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/align_stats.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `bam_urls` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/align_stats.done` exists and `bam_urls` can proceed without re-running align stats.
