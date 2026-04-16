---
name: finish-snakemake-workflows-chipseq-plot_heatmap
description: Use this skill when orchestrating the retained "plot_heatmap" step of the snakemake workflows chipseq finish finish workflow. It keeps the plot heatmap stage tied to upstream `plot_profile` and the downstream handoff to `phantompeakqualtools`. It tracks completion via `results/finish/plot_heatmap.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: plot_heatmap
  step_name: plot heatmap
---

# Scope
Use this skill only for the `plot_heatmap` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `plot_profile`
- Step file: `finish/chipseq-finish/steps/plot_heatmap.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plot_heatmap.done`
- Representative outputs: `results/finish/plot_heatmap.done`
- Execution targets: `plot_heatmap`
- Downstream handoff: `phantompeakqualtools`

## Guardrails
- Treat `results/finish/plot_heatmap.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plot_heatmap.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `phantompeakqualtools` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plot_heatmap.done` exists and `phantompeakqualtools` can proceed without re-running plot heatmap.
