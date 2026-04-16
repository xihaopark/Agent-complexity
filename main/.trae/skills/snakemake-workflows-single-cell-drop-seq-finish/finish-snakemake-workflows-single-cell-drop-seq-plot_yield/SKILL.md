---
name: finish-snakemake-workflows-single-cell-drop-seq-plot_yield
description: Use this skill when orchestrating the retained "plot_yield" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the plot yield stage tied to upstream `bam_hist` and the downstream handoff to `plot_knee_plot`. It tracks completion via `results/finish/plot_yield.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: plot_yield
  step_name: plot yield
---

# Scope
Use this skill only for the `plot_yield` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `bam_hist`
- Step file: `finish/single-cell-drop-seq-finish/steps/plot_yield.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plot_yield.done`
- Representative outputs: `results/finish/plot_yield.done`
- Execution targets: `plot_yield`
- Downstream handoff: `plot_knee_plot`

## Guardrails
- Treat `results/finish/plot_yield.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plot_yield.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plot_knee_plot` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plot_yield.done` exists and `plot_knee_plot` can proceed without re-running plot yield.
