---
name: finish-snakemake-workflows-single-cell-drop-seq-plot_knee_plot
description: Use this skill when orchestrating the retained "plot_knee_plot" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the plot knee plot stage tied to upstream `plot_yield` and the downstream handoff to `extract_umi_expression`. It tracks completion via `results/finish/plot_knee_plot.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: plot_knee_plot
  step_name: plot knee plot
---

# Scope
Use this skill only for the `plot_knee_plot` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `plot_yield`
- Step file: `finish/single-cell-drop-seq-finish/steps/plot_knee_plot.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plot_knee_plot.done`
- Representative outputs: `results/finish/plot_knee_plot.done`
- Execution targets: `plot_knee_plot`
- Downstream handoff: `extract_umi_expression`

## Guardrails
- Treat `results/finish/plot_knee_plot.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plot_knee_plot.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `extract_umi_expression` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plot_knee_plot.done` exists and `extract_umi_expression` can proceed without re-running plot knee plot.
