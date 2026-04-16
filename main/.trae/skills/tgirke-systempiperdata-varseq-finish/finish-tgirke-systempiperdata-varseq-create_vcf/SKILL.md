---
name: finish-tgirke-systempiperdata-varseq-create_vcf
description: Use this skill when orchestrating the retained "create_vcf" step of the tgirke systempiperdata varseq finish finish workflow. It keeps the create vcf stage tied to upstream `filter` and the downstream handoff to `filter_vcf`. It tracks completion via `results/finish/create_vcf.done`.
metadata:
  workflow_id: tgirke-systempiperdata-varseq-finish
  workflow_name: tgirke systempiperdata varseq finish
  step_id: create_vcf
  step_name: create vcf
---

# Scope
Use this skill only for the `create_vcf` step in `tgirke-systempiperdata-varseq-finish`.

## Orchestration
- Upstream requirements: `filter`
- Step file: `finish/tgirke-systempiperdata-varseq-finish/steps/create_vcf.smk`
- Config file: `finish/tgirke-systempiperdata-varseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/create_vcf.done`
- Representative outputs: `results/finish/create_vcf.done`
- Execution targets: `create_vcf`
- Downstream handoff: `filter_vcf`

## Guardrails
- Treat `results/finish/create_vcf.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/create_vcf.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `filter_vcf` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/create_vcf.done` exists and `filter_vcf` can proceed without re-running create vcf.
