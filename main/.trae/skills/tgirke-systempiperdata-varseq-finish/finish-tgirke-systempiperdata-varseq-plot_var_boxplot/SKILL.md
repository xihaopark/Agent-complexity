---
name: finish-tgirke-systempiperdata-varseq-plot_var_boxplot
description: Use this skill when orchestrating the retained "plot_var_boxplot" step of the tgirke systempiperdata varseq finish finish workflow. It keeps the plot var boxplot stage tied to upstream `plot_var_stats` and the downstream handoff to `venn_diagram`. It tracks completion via `results/finish/plot_var_boxplot.done`.
metadata:
  workflow_id: tgirke-systempiperdata-varseq-finish
  workflow_name: tgirke systempiperdata varseq finish
  step_id: plot_var_boxplot
  step_name: plot var boxplot
---

# Scope
Use this skill only for the `plot_var_boxplot` step in `tgirke-systempiperdata-varseq-finish`.

## Orchestration
- Upstream requirements: `plot_var_stats`
- Step file: `finish/tgirke-systempiperdata-varseq-finish/steps/plot_var_boxplot.smk`
- Config file: `finish/tgirke-systempiperdata-varseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plot_var_boxplot.done`
- Representative outputs: `results/finish/plot_var_boxplot.done`
- Execution targets: `plot_var_boxplot`
- Downstream handoff: `venn_diagram`

## Guardrails
- Treat `results/finish/plot_var_boxplot.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plot_var_boxplot.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `venn_diagram` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plot_var_boxplot.done` exists and `venn_diagram` can proceed without re-running plot var boxplot.
