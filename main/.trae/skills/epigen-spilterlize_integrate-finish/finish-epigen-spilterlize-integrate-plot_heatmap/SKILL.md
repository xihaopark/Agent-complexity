---
name: finish-epigen-spilterlize-integrate-plot_heatmap
description: Use this skill when orchestrating the retained "plot_heatmap" step of the epigen spilterlize_integrate finish finish workflow. It keeps the plot heatmap stage tied to upstream `plot_diagnostics` and the downstream handoff to `env_export`. It tracks completion via `results/finish/plot_heatmap.done`.
metadata:
  workflow_id: epigen-spilterlize_integrate-finish
  workflow_name: epigen spilterlize_integrate finish
  step_id: plot_heatmap
  step_name: plot heatmap
---

# Scope
Use this skill only for the `plot_heatmap` step in `epigen-spilterlize_integrate-finish`.

## Orchestration
- Upstream requirements: `plot_diagnostics`
- Step file: `finish/epigen-spilterlize_integrate-finish/steps/plot_heatmap.smk`
- Config file: `finish/epigen-spilterlize_integrate-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plot_heatmap.done`
- Representative outputs: `results/finish/plot_heatmap.done`
- Execution targets: `plot_heatmap`
- Downstream handoff: `env_export`

## Guardrails
- Treat `results/finish/plot_heatmap.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plot_heatmap.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `env_export` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plot_heatmap.done` exists and `env_export` can proceed without re-running plot heatmap.
