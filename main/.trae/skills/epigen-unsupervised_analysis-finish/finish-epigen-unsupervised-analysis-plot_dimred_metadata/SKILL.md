---
name: finish-epigen-unsupervised-analysis-plot_dimred_metadata
description: Use this skill when orchestrating the retained "plot_dimred_metadata" step of the epigen unsupervised_analysis finish finish workflow. It keeps the plot dimred metadata stage tied to upstream `plot_dimred_interactive` and the downstream handoff to `plot_heatmap`. It tracks completion via `results/finish/plot_dimred_metadata.done`.
metadata:
  workflow_id: epigen-unsupervised_analysis-finish
  workflow_name: epigen unsupervised_analysis finish
  step_id: plot_dimred_metadata
  step_name: plot dimred metadata
---

# Scope
Use this skill only for the `plot_dimred_metadata` step in `epigen-unsupervised_analysis-finish`.

## Orchestration
- Upstream requirements: `plot_dimred_interactive`
- Step file: `finish/epigen-unsupervised_analysis-finish/steps/plot_dimred_metadata.smk`
- Config file: `finish/epigen-unsupervised_analysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plot_dimred_metadata.done`
- Representative outputs: `results/finish/plot_dimred_metadata.done`
- Execution targets: `plot_dimred_metadata`
- Downstream handoff: `plot_heatmap`

## Guardrails
- Treat `results/finish/plot_dimred_metadata.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plot_dimred_metadata.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plot_heatmap` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plot_dimred_metadata.done` exists and `plot_heatmap` can proceed without re-running plot dimred metadata.
