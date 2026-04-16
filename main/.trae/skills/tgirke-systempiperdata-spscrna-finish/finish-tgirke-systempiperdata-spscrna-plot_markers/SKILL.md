---
name: finish-tgirke-systempiperdata-spscrna-plot_markers
description: Use this skill when orchestrating the retained "plot_markers" step of the tgirke systempiperdata spscrna finish finish workflow. It keeps the plot markers stage tied to upstream `find_markers` and the downstream handoff to `label_cell_type`. It tracks completion via `results/finish/plot_markers.done`.
metadata:
  workflow_id: tgirke-systempiperdata-spscrna-finish
  workflow_name: tgirke systempiperdata spscrna finish
  step_id: plot_markers
  step_name: plot markers
---

# Scope
Use this skill only for the `plot_markers` step in `tgirke-systempiperdata-spscrna-finish`.

## Orchestration
- Upstream requirements: `find_markers`
- Step file: `finish/tgirke-systempiperdata-spscrna-finish/steps/plot_markers.smk`
- Config file: `finish/tgirke-systempiperdata-spscrna-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plot_markers.done`
- Representative outputs: `results/finish/plot_markers.done`
- Execution targets: `plot_markers`
- Downstream handoff: `label_cell_type`

## Guardrails
- Treat `results/finish/plot_markers.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plot_markers.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `label_cell_type` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plot_markers.done` exists and `label_cell_type` can proceed without re-running plot markers.
