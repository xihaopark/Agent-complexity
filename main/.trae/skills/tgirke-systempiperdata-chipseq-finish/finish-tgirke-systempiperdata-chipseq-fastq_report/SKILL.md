---
name: finish-tgirke-systempiperdata-chipseq-fastq_report
description: Use this skill when orchestrating the retained "fastq_report" step of the tgirke systempiperdata chipseq finish finish workflow. It keeps the fastq report stage tied to upstream `load_SPR` and the downstream handoff to `preprocessing`. It tracks completion via `results/finish/fastq_report.done`.
metadata:
  workflow_id: tgirke-systempiperdata-chipseq-finish
  workflow_name: tgirke systempiperdata chipseq finish
  step_id: fastq_report
  step_name: fastq report
---

# Scope
Use this skill only for the `fastq_report` step in `tgirke-systempiperdata-chipseq-finish`.

## Orchestration
- Upstream requirements: `load_SPR`
- Step file: `finish/tgirke-systempiperdata-chipseq-finish/steps/fastq_report.smk`
- Config file: `finish/tgirke-systempiperdata-chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/fastq_report.done`
- Representative outputs: `results/finish/fastq_report.done`
- Execution targets: `fastq_report`
- Downstream handoff: `preprocessing`

## Guardrails
- Treat `results/finish/fastq_report.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/fastq_report.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `preprocessing` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/fastq_report.done` exists and `preprocessing` can proceed without re-running fastq report.
