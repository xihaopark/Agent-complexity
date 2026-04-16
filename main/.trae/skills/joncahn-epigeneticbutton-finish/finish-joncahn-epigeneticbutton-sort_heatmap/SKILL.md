---
name: finish-joncahn-epigeneticbutton-sort_heatmap
description: Use this skill when orchestrating the retained "sort_heatmap" step of the joncahn epigeneticbutton finish finish workflow. It keeps the sort heatmap stage tied to upstream `plotting_heatmap_on_targetfile` and the downstream handoff to `plotting_sorted_heatmap_on_targetfile`. It tracks completion via `results/finish/sort_heatmap.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: sort_heatmap
  step_name: sort heatmap
---

# Scope
Use this skill only for the `sort_heatmap` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `plotting_heatmap_on_targetfile`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/sort_heatmap.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/sort_heatmap.done`
- Representative outputs: `results/finish/sort_heatmap.done`
- Execution targets: `sort_heatmap`
- Downstream handoff: `plotting_sorted_heatmap_on_targetfile`

## Guardrails
- Treat `results/finish/sort_heatmap.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/sort_heatmap.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plotting_sorted_heatmap_on_targetfile` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/sort_heatmap.done` exists and `plotting_sorted_heatmap_on_targetfile` can proceed without re-running sort heatmap.
