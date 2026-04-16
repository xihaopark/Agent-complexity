---
name: finish-tgirke-systempiperdata-rnaseq-fastq_report
description: Use this skill when orchestrating the retained "fastq_report" step of the tgirke systempiperdata rnaseq finish finish workflow. It keeps the fastq report stage tied to upstream `trimming` and the downstream handoff to `hisat2_index`. It tracks completion via `results/finish/fastq_report.done`.
metadata:
  workflow_id: tgirke-systempiperdata-rnaseq-finish
  workflow_name: tgirke systempiperdata rnaseq finish
  step_id: fastq_report
  step_name: fastq report
---

# Scope
Use this skill only for the `fastq_report` step in `tgirke-systempiperdata-rnaseq-finish`.

## Orchestration
- Upstream requirements: `trimming`
- Step file: `finish/tgirke-systempiperdata-rnaseq-finish/steps/fastq_report.smk`
- Config file: `finish/tgirke-systempiperdata-rnaseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/fastq_report.done`
- Representative outputs: `results/finish/fastq_report.done`
- Execution targets: `fastq_report`
- Downstream handoff: `hisat2_index`

## Guardrails
- Treat `results/finish/fastq_report.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/fastq_report.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `hisat2_index` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/fastq_report.done` exists and `hisat2_index` can proceed without re-running fastq report.
