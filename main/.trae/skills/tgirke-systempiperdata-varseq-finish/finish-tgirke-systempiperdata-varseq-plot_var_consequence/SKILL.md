---
name: finish-tgirke-systempiperdata-varseq-plot_var_consequence
description: Use this skill when orchestrating the retained "plot_var_consequence" step of the tgirke systempiperdata varseq finish finish workflow. It keeps the plot var consequence stage tied to upstream `summary_var` and the downstream handoff to `plot_var_stats`. It tracks completion via `results/finish/plot_var_consequence.done`.
metadata:
  workflow_id: tgirke-systempiperdata-varseq-finish
  workflow_name: tgirke systempiperdata varseq finish
  step_id: plot_var_consequence
  step_name: plot var consequence
---

# Scope
Use this skill only for the `plot_var_consequence` step in `tgirke-systempiperdata-varseq-finish`.

## Orchestration
- Upstream requirements: `summary_var`
- Step file: `finish/tgirke-systempiperdata-varseq-finish/steps/plot_var_consequence.smk`
- Config file: `finish/tgirke-systempiperdata-varseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plot_var_consequence.done`
- Representative outputs: `results/finish/plot_var_consequence.done`
- Execution targets: `plot_var_consequence`
- Downstream handoff: `plot_var_stats`

## Guardrails
- Treat `results/finish/plot_var_consequence.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plot_var_consequence.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plot_var_stats` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plot_var_consequence.done` exists and `plot_var_stats` can proceed without re-running plot var consequence.
