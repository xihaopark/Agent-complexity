---
name: finish-tgirke-systempiperdata-rnaseq-trimming
description: Use this skill when orchestrating the retained "trimming" step of the tgirke systempiperdata rnaseq finish finish workflow. It keeps the trimming stage tied to upstream `custom_preprocessing_function` and the downstream handoff to `fastq_report`. It tracks completion via `results/finish/trimming.done`.
metadata:
  workflow_id: tgirke-systempiperdata-rnaseq-finish
  workflow_name: tgirke systempiperdata rnaseq finish
  step_id: trimming
  step_name: trimming
---

# Scope
Use this skill only for the `trimming` step in `tgirke-systempiperdata-rnaseq-finish`.

## Orchestration
- Upstream requirements: `custom_preprocessing_function`
- Step file: `finish/tgirke-systempiperdata-rnaseq-finish/steps/trimming.smk`
- Config file: `finish/tgirke-systempiperdata-rnaseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/trimming.done`
- Representative outputs: `results/finish/trimming.done`
- Execution targets: `trimming`
- Downstream handoff: `fastq_report`

## Guardrails
- Treat `results/finish/trimming.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/trimming.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `fastq_report` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/trimming.done` exists and `fastq_report` can proceed without re-running trimming.
