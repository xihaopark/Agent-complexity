---
name: finish-tgirke-systempiperdata-riboseq-hisat2_index
description: Use this skill when orchestrating the retained "hisat2_index" step of the tgirke systempiperdata riboseq finish finish workflow. It keeps the hisat2 index stage tied to upstream `fastq_report` and the downstream handoff to `hisat2_mapping`. It tracks completion via `results/finish/hisat2_index.done`.
metadata:
  workflow_id: tgirke-systempiperdata-riboseq-finish
  workflow_name: tgirke systempiperdata riboseq finish
  step_id: hisat2_index
  step_name: hisat2 index
---

# Scope
Use this skill only for the `hisat2_index` step in `tgirke-systempiperdata-riboseq-finish`.

## Orchestration
- Upstream requirements: `fastq_report`
- Step file: `finish/tgirke-systempiperdata-riboseq-finish/steps/hisat2_index.smk`
- Config file: `finish/tgirke-systempiperdata-riboseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/hisat2_index.done`
- Representative outputs: `results/finish/hisat2_index.done`
- Execution targets: `hisat2_index`
- Downstream handoff: `hisat2_mapping`

## Guardrails
- Treat `results/finish/hisat2_index.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/hisat2_index.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `hisat2_mapping` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/hisat2_index.done` exists and `hisat2_mapping` can proceed without re-running hisat2 index.
