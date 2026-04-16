---
name: finish-joncahn-epigeneticbutton-merge_region_browser_plots
description: Use this skill when orchestrating the retained "merge_region_browser_plots" step of the joncahn epigeneticbutton finish finish workflow. It keeps the merge region browser plots stage tied to upstream `make_single_loci_browser_plot` and the downstream handoff to `summarize_tracks_pca`. It tracks completion via `results/finish/merge_region_browser_plots.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: merge_region_browser_plots
  step_name: merge region browser plots
---

# Scope
Use this skill only for the `merge_region_browser_plots` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `make_single_loci_browser_plot`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/merge_region_browser_plots.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/merge_region_browser_plots.done`
- Representative outputs: `results/finish/merge_region_browser_plots.done`
- Execution targets: `merge_region_browser_plots`
- Downstream handoff: `summarize_tracks_pca`

## Guardrails
- Treat `results/finish/merge_region_browser_plots.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/merge_region_browser_plots.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `summarize_tracks_pca` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/merge_region_browser_plots.done` exists and `summarize_tracks_pca` can proceed without re-running merge region browser plots.
