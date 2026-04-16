---
name: finish-tgirke-systempiperdata-riboseq-bam_igv
description: Use this skill when orchestrating the retained "bam_IGV" step of the tgirke systempiperdata riboseq finish finish workflow. It keeps the bam IGV stage tied to upstream `align_stats` and the downstream handoff to `genFeatures`. It tracks completion via `results/finish/bam_IGV.done`.
metadata:
  workflow_id: tgirke-systempiperdata-riboseq-finish
  workflow_name: tgirke systempiperdata riboseq finish
  step_id: bam_IGV
  step_name: bam IGV
---

# Scope
Use this skill only for the `bam_IGV` step in `tgirke-systempiperdata-riboseq-finish`.

## Orchestration
- Upstream requirements: `align_stats`
- Step file: `finish/tgirke-systempiperdata-riboseq-finish/steps/bam_IGV.smk`
- Config file: `finish/tgirke-systempiperdata-riboseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/bam_IGV.done`
- Representative outputs: `results/finish/bam_IGV.done`
- Execution targets: `bam_IGV`
- Downstream handoff: `genFeatures`

## Guardrails
- Treat `results/finish/bam_IGV.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/bam_IGV.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `genFeatures` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/bam_IGV.done` exists and `genFeatures` can proceed without re-running bam IGV.
