---
name: finish-tgirke-systempiperdata-varseq-filter
description: Use this skill when orchestrating the retained "filter" step of the tgirke systempiperdata varseq finish finish workflow. It keeps the filter stage tied to upstream `call_variants` and the downstream handoff to `create_vcf`. It tracks completion via `results/finish/filter.done`.
metadata:
  workflow_id: tgirke-systempiperdata-varseq-finish
  workflow_name: tgirke systempiperdata varseq finish
  step_id: filter
  step_name: filter
---

# Scope
Use this skill only for the `filter` step in `tgirke-systempiperdata-varseq-finish`.

## Orchestration
- Upstream requirements: `call_variants`
- Step file: `finish/tgirke-systempiperdata-varseq-finish/steps/filter.smk`
- Config file: `finish/tgirke-systempiperdata-varseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/filter.done`
- Representative outputs: `results/finish/filter.done`
- Execution targets: `filter`
- Downstream handoff: `create_vcf`

## Guardrails
- Treat `results/finish/filter.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/filter.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `create_vcf` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/filter.done` exists and `create_vcf` can proceed without re-running filter.
