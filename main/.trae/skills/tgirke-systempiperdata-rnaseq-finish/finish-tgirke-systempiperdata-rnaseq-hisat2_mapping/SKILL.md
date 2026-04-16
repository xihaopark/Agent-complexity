---
name: finish-tgirke-systempiperdata-rnaseq-hisat2_mapping
description: Use this skill when orchestrating the retained "hisat2_mapping" step of the tgirke systempiperdata rnaseq finish finish workflow. It keeps the hisat2 mapping stage tied to upstream `hisat2_index` and the downstream handoff to `align_stats`. It tracks completion via `results/finish/hisat2_mapping.done`.
metadata:
  workflow_id: tgirke-systempiperdata-rnaseq-finish
  workflow_name: tgirke systempiperdata rnaseq finish
  step_id: hisat2_mapping
  step_name: hisat2 mapping
---

# Scope
Use this skill only for the `hisat2_mapping` step in `tgirke-systempiperdata-rnaseq-finish`.

## Orchestration
- Upstream requirements: `hisat2_index`
- Step file: `finish/tgirke-systempiperdata-rnaseq-finish/steps/hisat2_mapping.smk`
- Config file: `finish/tgirke-systempiperdata-rnaseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/hisat2_mapping.done`
- Representative outputs: `results/finish/hisat2_mapping.done`
- Execution targets: `hisat2_mapping`
- Downstream handoff: `align_stats`

## Guardrails
- Treat `results/finish/hisat2_mapping.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/hisat2_mapping.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `align_stats` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/hisat2_mapping.done` exists and `align_stats` can proceed without re-running hisat2 mapping.
