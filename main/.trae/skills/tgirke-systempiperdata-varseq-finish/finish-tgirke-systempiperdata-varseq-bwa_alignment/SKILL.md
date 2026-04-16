---
name: finish-tgirke-systempiperdata-varseq-bwa_alignment
description: Use this skill when orchestrating the retained "bwa_alignment" step of the tgirke systempiperdata varseq finish finish workflow. It keeps the bwa alignment stage tied to upstream `faidx_index` and the downstream handoff to `align_stats`. It tracks completion via `results/finish/bwa_alignment.done`.
metadata:
  workflow_id: tgirke-systempiperdata-varseq-finish
  workflow_name: tgirke systempiperdata varseq finish
  step_id: bwa_alignment
  step_name: bwa alignment
---

# Scope
Use this skill only for the `bwa_alignment` step in `tgirke-systempiperdata-varseq-finish`.

## Orchestration
- Upstream requirements: `faidx_index`
- Step file: `finish/tgirke-systempiperdata-varseq-finish/steps/bwa_alignment.smk`
- Config file: `finish/tgirke-systempiperdata-varseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/bwa_alignment.done`
- Representative outputs: `results/finish/bwa_alignment.done`
- Execution targets: `bwa_alignment`
- Downstream handoff: `align_stats`

## Guardrails
- Treat `results/finish/bwa_alignment.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/bwa_alignment.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `align_stats` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/bwa_alignment.done` exists and `align_stats` can proceed without re-running bwa alignment.
