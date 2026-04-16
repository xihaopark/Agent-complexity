---
name: finish-snakemake-workflows-cyrcular-calling-circle_graph_plots
description: Use this skill when orchestrating the retained "circle_graph_plots" step of the snakemake workflows cyrcular calling finish finish workflow. It keeps the circle graph plots stage tied to upstream `circle_coverage_plot` and the downstream handoff to `render_datavzrd_config`. It tracks completion via `results/finish/circle_graph_plots.done`.
metadata:
  workflow_id: cyrcular-calling-finish
  workflow_name: snakemake workflows cyrcular calling finish
  step_id: circle_graph_plots
  step_name: circle graph plots
---

# Scope
Use this skill only for the `circle_graph_plots` step in `cyrcular-calling-finish`.

## Orchestration
- Upstream requirements: `circle_coverage_plot`
- Step file: `finish/cyrcular-calling-finish/steps/circle_graph_plots.smk`
- Config file: `finish/cyrcular-calling-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/circle_graph_plots.done`
- Representative outputs: `results/finish/circle_graph_plots.done`
- Execution targets: `circle_graph_plots`
- Downstream handoff: `render_datavzrd_config`

## Guardrails
- Treat `results/finish/circle_graph_plots.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/circle_graph_plots.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `render_datavzrd_config` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/circle_graph_plots.done` exists and `render_datavzrd_config` can proceed without re-running circle graph plots.
