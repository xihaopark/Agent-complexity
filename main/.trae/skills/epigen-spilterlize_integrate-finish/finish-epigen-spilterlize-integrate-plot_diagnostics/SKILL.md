---
name: finish-epigen-spilterlize-integrate-plot_diagnostics
description: Use this skill when orchestrating the retained "plot_diagnostics" step of the epigen spilterlize_integrate finish finish workflow. It keeps the plot diagnostics stage tied to upstream `plot_cfa` and the downstream handoff to `plot_heatmap`. It tracks completion via `results/finish/plot_diagnostics.done`.
metadata:
  workflow_id: epigen-spilterlize_integrate-finish
  workflow_name: epigen spilterlize_integrate finish
  step_id: plot_diagnostics
  step_name: plot diagnostics
---

# Scope
Use this skill only for the `plot_diagnostics` step in `epigen-spilterlize_integrate-finish`.

## Orchestration
- Upstream requirements: `plot_cfa`
- Step file: `finish/epigen-spilterlize_integrate-finish/steps/plot_diagnostics.smk`
- Config file: `finish/epigen-spilterlize_integrate-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plot_diagnostics.done`
- Representative outputs: `results/finish/plot_diagnostics.done`
- Execution targets: `plot_diagnostics`
- Downstream handoff: `plot_heatmap`

## Guardrails
- Treat `results/finish/plot_diagnostics.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plot_diagnostics.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plot_heatmap` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plot_diagnostics.done` exists and `plot_heatmap` can proceed without re-running plot diagnostics.
