---
name: finish-joncahn-epigeneticbutton-plot_pca_correlation
description: Use this skill when orchestrating the retained "plot_PCA_correlation" step of the joncahn epigeneticbutton finish finish workflow. It keeps the plot PCA correlation stage tied to upstream `summarize_tracks_pca` and the downstream handoff to `all_combined`. It tracks completion via `results/finish/plot_PCA_correlation.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: plot_PCA_correlation
  step_name: plot PCA correlation
---

# Scope
Use this skill only for the `plot_PCA_correlation` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `summarize_tracks_pca`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/plot_PCA_correlation.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plot_PCA_correlation.done`
- Representative outputs: `results/finish/plot_PCA_correlation.done`
- Execution targets: `plot_PCA_correlation`
- Downstream handoff: `all_combined`

## Guardrails
- Treat `results/finish/plot_PCA_correlation.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plot_PCA_correlation.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `all_combined` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plot_PCA_correlation.done` exists and `all_combined` can proceed without re-running plot PCA correlation.
