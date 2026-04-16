---
name: finish-tgirke-systempiperdata-varseq-summary_filter
description: Use this skill when orchestrating the retained "summary_filter" step of the tgirke systempiperdata varseq finish finish workflow. It keeps the summary filter stage tied to upstream `filter_vcf` and the downstream handoff to `annotate_vcf`. It tracks completion via `results/finish/summary_filter.done`.
metadata:
  workflow_id: tgirke-systempiperdata-varseq-finish
  workflow_name: tgirke systempiperdata varseq finish
  step_id: summary_filter
  step_name: summary filter
---

# Scope
Use this skill only for the `summary_filter` step in `tgirke-systempiperdata-varseq-finish`.

## Orchestration
- Upstream requirements: `filter_vcf`
- Step file: `finish/tgirke-systempiperdata-varseq-finish/steps/summary_filter.smk`
- Config file: `finish/tgirke-systempiperdata-varseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/summary_filter.done`
- Representative outputs: `results/finish/summary_filter.done`
- Execution targets: `summary_filter`
- Downstream handoff: `annotate_vcf`

## Guardrails
- Treat `results/finish/summary_filter.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/summary_filter.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `annotate_vcf` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/summary_filter.done` exists and `annotate_vcf` can proceed without re-running summary filter.
