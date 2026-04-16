---
name: finish-tgirke-systempiperdata-varseq-summary_var
description: Use this skill when orchestrating the retained "summary_var" step of the tgirke systempiperdata varseq finish finish workflow. It keeps the summary var stage tied to upstream `combine_var` and the downstream handoff to `plot_var_consequence`. It tracks completion via `results/finish/summary_var.done`.
metadata:
  workflow_id: tgirke-systempiperdata-varseq-finish
  workflow_name: tgirke systempiperdata varseq finish
  step_id: summary_var
  step_name: summary var
---

# Scope
Use this skill only for the `summary_var` step in `tgirke-systempiperdata-varseq-finish`.

## Orchestration
- Upstream requirements: `combine_var`
- Step file: `finish/tgirke-systempiperdata-varseq-finish/steps/summary_var.smk`
- Config file: `finish/tgirke-systempiperdata-varseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/summary_var.done`
- Representative outputs: `results/finish/summary_var.done`
- Execution targets: `summary_var`
- Downstream handoff: `plot_var_consequence`

## Guardrails
- Treat `results/finish/summary_var.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/summary_var.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plot_var_consequence` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/summary_var.done` exists and `plot_var_consequence` can proceed without re-running summary var.
