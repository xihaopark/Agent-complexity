---
name: finish-joncahn-epigeneticbutton-summarize_tracks_pca
description: Use this skill when orchestrating the retained "summarize_tracks_pca" step of the joncahn epigeneticbutton finish finish workflow. It keeps the summarize tracks pca stage tied to upstream `merge_region_browser_plots` and the downstream handoff to `plot_PCA_correlation`. It tracks completion via `results/finish/summarize_tracks_pca.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: summarize_tracks_pca
  step_name: summarize tracks pca
---

# Scope
Use this skill only for the `summarize_tracks_pca` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `merge_region_browser_plots`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/summarize_tracks_pca.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/summarize_tracks_pca.done`
- Representative outputs: `results/finish/summarize_tracks_pca.done`
- Execution targets: `summarize_tracks_pca`
- Downstream handoff: `plot_PCA_correlation`

## Guardrails
- Treat `results/finish/summarize_tracks_pca.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/summarize_tracks_pca.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plot_PCA_correlation` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/summarize_tracks_pca.done` exists and `plot_PCA_correlation` can proceed without re-running summarize tracks pca.
