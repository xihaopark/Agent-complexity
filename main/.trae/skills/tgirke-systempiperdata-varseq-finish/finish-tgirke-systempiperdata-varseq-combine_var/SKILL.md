---
name: finish-tgirke-systempiperdata-varseq-combine_var
description: Use this skill when orchestrating the retained "combine_var" step of the tgirke systempiperdata varseq finish finish workflow. It keeps the combine var stage tied to upstream `annotate_vcf` and the downstream handoff to `summary_var`. It tracks completion via `results/finish/combine_var.done`.
metadata:
  workflow_id: tgirke-systempiperdata-varseq-finish
  workflow_name: tgirke systempiperdata varseq finish
  step_id: combine_var
  step_name: combine var
---

# Scope
Use this skill only for the `combine_var` step in `tgirke-systempiperdata-varseq-finish`.

## Orchestration
- Upstream requirements: `annotate_vcf`
- Step file: `finish/tgirke-systempiperdata-varseq-finish/steps/combine_var.smk`
- Config file: `finish/tgirke-systempiperdata-varseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/combine_var.done`
- Representative outputs: `results/finish/combine_var.done`
- Execution targets: `combine_var`
- Downstream handoff: `summary_var`

## Guardrails
- Treat `results/finish/combine_var.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/combine_var.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `summary_var` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/combine_var.done` exists and `summary_var` can proceed without re-running combine var.
