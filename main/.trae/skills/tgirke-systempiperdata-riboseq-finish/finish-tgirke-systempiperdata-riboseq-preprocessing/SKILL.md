---
name: finish-tgirke-systempiperdata-riboseq-preprocessing
description: Use this skill when orchestrating the retained "preprocessing" step of the tgirke systempiperdata riboseq finish finish workflow. It keeps the preprocessing stage tied to upstream `load_SPR` and the downstream handoff to `fastq_report`. It tracks completion via `results/finish/preprocessing.done`.
metadata:
  workflow_id: tgirke-systempiperdata-riboseq-finish
  workflow_name: tgirke systempiperdata riboseq finish
  step_id: preprocessing
  step_name: preprocessing
---

# Scope
Use this skill only for the `preprocessing` step in `tgirke-systempiperdata-riboseq-finish`.

## Orchestration
- Upstream requirements: `load_SPR`
- Step file: `finish/tgirke-systempiperdata-riboseq-finish/steps/preprocessing.smk`
- Config file: `finish/tgirke-systempiperdata-riboseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/preprocessing.done`
- Representative outputs: `results/finish/preprocessing.done`
- Execution targets: `preprocessing`
- Downstream handoff: `fastq_report`

## Guardrails
- Treat `results/finish/preprocessing.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/preprocessing.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `fastq_report` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/preprocessing.done` exists and `fastq_report` can proceed without re-running preprocessing.
