---
name: finish-tgirke-systempiperdata-chipseq-preprocessing
description: Use this skill when orchestrating the retained "preprocessing" step of the tgirke systempiperdata chipseq finish finish workflow. It keeps the preprocessing stage tied to upstream `fastq_report` and the downstream handoff to `custom_preprocessing_function`. It tracks completion via `results/finish/preprocessing.done`.
metadata:
  workflow_id: tgirke-systempiperdata-chipseq-finish
  workflow_name: tgirke systempiperdata chipseq finish
  step_id: preprocessing
  step_name: preprocessing
---

# Scope
Use this skill only for the `preprocessing` step in `tgirke-systempiperdata-chipseq-finish`.

## Orchestration
- Upstream requirements: `fastq_report`
- Step file: `finish/tgirke-systempiperdata-chipseq-finish/steps/preprocessing.smk`
- Config file: `finish/tgirke-systempiperdata-chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/preprocessing.done`
- Representative outputs: `results/finish/preprocessing.done`
- Execution targets: `preprocessing`
- Downstream handoff: `custom_preprocessing_function`

## Guardrails
- Treat `results/finish/preprocessing.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/preprocessing.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `custom_preprocessing_function` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/preprocessing.done` exists and `custom_preprocessing_function` can proceed without re-running preprocessing.
