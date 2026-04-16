---
name: finish-tgirke-systempiperdata-varseq-filter_vcf
description: Use this skill when orchestrating the retained "filter_vcf" step of the tgirke systempiperdata varseq finish finish workflow. It keeps the filter vcf stage tied to upstream `create_vcf` and the downstream handoff to `summary_filter`. It tracks completion via `results/finish/filter_vcf.done`.
metadata:
  workflow_id: tgirke-systempiperdata-varseq-finish
  workflow_name: tgirke systempiperdata varseq finish
  step_id: filter_vcf
  step_name: filter vcf
---

# Scope
Use this skill only for the `filter_vcf` step in `tgirke-systempiperdata-varseq-finish`.

## Orchestration
- Upstream requirements: `create_vcf`
- Step file: `finish/tgirke-systempiperdata-varseq-finish/steps/filter_vcf.smk`
- Config file: `finish/tgirke-systempiperdata-varseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/filter_vcf.done`
- Representative outputs: `results/finish/filter_vcf.done`
- Execution targets: `filter_vcf`
- Downstream handoff: `summary_filter`

## Guardrails
- Treat `results/finish/filter_vcf.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/filter_vcf.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `summary_filter` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/filter_vcf.done` exists and `summary_filter` can proceed without re-running filter vcf.
