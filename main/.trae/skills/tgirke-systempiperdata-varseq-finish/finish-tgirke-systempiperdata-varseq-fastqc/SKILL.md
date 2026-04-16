---
name: finish-tgirke-systempiperdata-varseq-fastqc
description: Use this skill when orchestrating the retained "fastqc" step of the tgirke systempiperdata varseq finish finish workflow. It keeps the fastqc stage tied to upstream `load_SPR` and the downstream handoff to `fastq_report`. It tracks completion via `results/finish/fastqc.done`.
metadata:
  workflow_id: tgirke-systempiperdata-varseq-finish
  workflow_name: tgirke systempiperdata varseq finish
  step_id: fastqc
  step_name: fastqc
---

# Scope
Use this skill only for the `fastqc` step in `tgirke-systempiperdata-varseq-finish`.

## Orchestration
- Upstream requirements: `load_SPR`
- Step file: `finish/tgirke-systempiperdata-varseq-finish/steps/fastqc.smk`
- Config file: `finish/tgirke-systempiperdata-varseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/fastqc.done`
- Representative outputs: `results/finish/fastqc.done`
- Execution targets: `fastqc`
- Downstream handoff: `fastq_report`

## Guardrails
- Treat `results/finish/fastqc.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/fastqc.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `fastq_report` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/fastqc.done` exists and `fastq_report` can proceed without re-running fastqc.
