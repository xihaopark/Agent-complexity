---
name: finish-tgirke-systempiperdata-varseq-annotate_vcf
description: Use this skill when orchestrating the retained "annotate_vcf" step of the tgirke systempiperdata varseq finish finish workflow. It keeps the annotate vcf stage tied to upstream `summary_filter` and the downstream handoff to `combine_var`. It tracks completion via `results/finish/annotate_vcf.done`.
metadata:
  workflow_id: tgirke-systempiperdata-varseq-finish
  workflow_name: tgirke systempiperdata varseq finish
  step_id: annotate_vcf
  step_name: annotate vcf
---

# Scope
Use this skill only for the `annotate_vcf` step in `tgirke-systempiperdata-varseq-finish`.

## Orchestration
- Upstream requirements: `summary_filter`
- Step file: `finish/tgirke-systempiperdata-varseq-finish/steps/annotate_vcf.smk`
- Config file: `finish/tgirke-systempiperdata-varseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/annotate_vcf.done`
- Representative outputs: `results/finish/annotate_vcf.done`
- Execution targets: `annotate_vcf`
- Downstream handoff: `combine_var`

## Guardrails
- Treat `results/finish/annotate_vcf.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/annotate_vcf.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `combine_var` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/annotate_vcf.done` exists and `combine_var` can proceed without re-running annotate vcf.
