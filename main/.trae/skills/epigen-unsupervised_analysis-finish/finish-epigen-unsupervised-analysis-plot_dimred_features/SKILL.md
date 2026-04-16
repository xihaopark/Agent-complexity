---
name: finish-epigen-unsupervised-analysis-plot_dimred_features
description: Use this skill when orchestrating the retained "plot_dimred_features" step of the epigen unsupervised_analysis finish finish workflow. It keeps the plot dimred features stage tied to upstream `plot_dimred_clustering` and the downstream handoff to `plot_dimred_interactive`. It tracks completion via `results/finish/plot_dimred_features.done`.
metadata:
  workflow_id: epigen-unsupervised_analysis-finish
  workflow_name: epigen unsupervised_analysis finish
  step_id: plot_dimred_features
  step_name: plot dimred features
---

# Scope
Use this skill only for the `plot_dimred_features` step in `epigen-unsupervised_analysis-finish`.

## Orchestration
- Upstream requirements: `plot_dimred_clustering`
- Step file: `finish/epigen-unsupervised_analysis-finish/steps/plot_dimred_features.smk`
- Config file: `finish/epigen-unsupervised_analysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plot_dimred_features.done`
- Representative outputs: `results/finish/plot_dimred_features.done`
- Execution targets: `plot_dimred_features`
- Downstream handoff: `plot_dimred_interactive`

## Guardrails
- Treat `results/finish/plot_dimred_features.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plot_dimred_features.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plot_dimred_interactive` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plot_dimred_features.done` exists and `plot_dimred_interactive` can proceed without re-running plot dimred features.
