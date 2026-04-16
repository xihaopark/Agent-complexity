---
name: finish-tgirke-systempiperdata-varseq-plot_var_stats
description: Use this skill when orchestrating the retained "plot_var_stats" step of the tgirke systempiperdata varseq finish finish workflow. It keeps the plot var stats stage tied to upstream `plot_var_consequence` and the downstream handoff to `plot_var_boxplot`. It tracks completion via `results/finish/plot_var_stats.done`.
metadata:
  workflow_id: tgirke-systempiperdata-varseq-finish
  workflow_name: tgirke systempiperdata varseq finish
  step_id: plot_var_stats
  step_name: plot var stats
---

# Scope
Use this skill only for the `plot_var_stats` step in `tgirke-systempiperdata-varseq-finish`.

## Orchestration
- Upstream requirements: `plot_var_consequence`
- Step file: `finish/tgirke-systempiperdata-varseq-finish/steps/plot_var_stats.smk`
- Config file: `finish/tgirke-systempiperdata-varseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plot_var_stats.done`
- Representative outputs: `results/finish/plot_var_stats.done`
- Execution targets: `plot_var_stats`
- Downstream handoff: `plot_var_boxplot`

## Guardrails
- Treat `results/finish/plot_var_stats.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plot_var_stats.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plot_var_boxplot` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plot_var_stats.done` exists and `plot_var_boxplot` can proceed without re-running plot var stats.
