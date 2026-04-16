---
name: finish-tgirke-systempiperdata-chipseq-bowtie2_alignment
description: Use this skill when orchestrating the retained "bowtie2_alignment" step of the tgirke systempiperdata chipseq finish finish workflow. It keeps the bowtie2 alignment stage tied to upstream `bowtie2_index` and the downstream handoff to `align_stats`. It tracks completion via `results/finish/bowtie2_alignment.done`.
metadata:
  workflow_id: tgirke-systempiperdata-chipseq-finish
  workflow_name: tgirke systempiperdata chipseq finish
  step_id: bowtie2_alignment
  step_name: bowtie2 alignment
---

# Scope
Use this skill only for the `bowtie2_alignment` step in `tgirke-systempiperdata-chipseq-finish`.

## Orchestration
- Upstream requirements: `bowtie2_index`
- Step file: `finish/tgirke-systempiperdata-chipseq-finish/steps/bowtie2_alignment.smk`
- Config file: `finish/tgirke-systempiperdata-chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/bowtie2_alignment.done`
- Representative outputs: `results/finish/bowtie2_alignment.done`
- Execution targets: `bowtie2_alignment`
- Downstream handoff: `align_stats`

## Guardrails
- Treat `results/finish/bowtie2_alignment.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/bowtie2_alignment.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `align_stats` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/bowtie2_alignment.done` exists and `align_stats` can proceed without re-running bowtie2 alignment.
