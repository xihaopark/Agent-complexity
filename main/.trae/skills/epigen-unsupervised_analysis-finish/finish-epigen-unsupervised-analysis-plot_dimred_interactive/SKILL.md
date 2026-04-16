---
name: finish-epigen-unsupervised-analysis-plot_dimred_interactive
description: Use this skill when orchestrating the retained "plot_dimred_interactive" step of the epigen unsupervised_analysis finish finish workflow. It keeps the plot dimred interactive stage tied to upstream `plot_dimred_features` and the downstream handoff to `plot_dimred_metadata`. It tracks completion via `results/finish/plot_dimred_interactive.done`.
metadata:
  workflow_id: epigen-unsupervised_analysis-finish
  workflow_name: epigen unsupervised_analysis finish
  step_id: plot_dimred_interactive
  step_name: plot dimred interactive
---

# Scope
Use this skill only for the `plot_dimred_interactive` step in `epigen-unsupervised_analysis-finish`.

## Orchestration
- Upstream requirements: `plot_dimred_features`
- Step file: `finish/epigen-unsupervised_analysis-finish/steps/plot_dimred_interactive.smk`
- Config file: `finish/epigen-unsupervised_analysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plot_dimred_interactive.done`
- Representative outputs: `results/finish/plot_dimred_interactive.done`
- Execution targets: `plot_dimred_interactive`
- Downstream handoff: `plot_dimred_metadata`

## Guardrails
- Treat `results/finish/plot_dimred_interactive.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plot_dimred_interactive.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plot_dimred_metadata` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plot_dimred_interactive.done` exists and `plot_dimred_metadata` can proceed without re-running plot dimred interactive.
