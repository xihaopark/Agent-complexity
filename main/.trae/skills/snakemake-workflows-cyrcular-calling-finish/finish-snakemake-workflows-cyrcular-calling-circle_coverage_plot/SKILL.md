---
name: finish-snakemake-workflows-cyrcular-calling-circle_coverage_plot
description: Use this skill when orchestrating the retained "circle_coverage_plot" step of the snakemake workflows cyrcular calling finish finish workflow. It keeps the circle coverage plot stage tied to upstream `filter_varlociraptor` and the downstream handoff to `circle_graph_plots`. It tracks completion via `results/finish/circle_coverage_plot.done`.
metadata:
  workflow_id: cyrcular-calling-finish
  workflow_name: snakemake workflows cyrcular calling finish
  step_id: circle_coverage_plot
  step_name: circle coverage plot
---

# Scope
Use this skill only for the `circle_coverage_plot` step in `cyrcular-calling-finish`.

## Orchestration
- Upstream requirements: `filter_varlociraptor`
- Step file: `finish/cyrcular-calling-finish/steps/circle_coverage_plot.smk`
- Config file: `finish/cyrcular-calling-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/circle_coverage_plot.done`
- Representative outputs: `results/finish/circle_coverage_plot.done`
- Execution targets: `circle_coverage_plot`
- Downstream handoff: `circle_graph_plots`

## Guardrails
- Treat `results/finish/circle_coverage_plot.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/circle_coverage_plot.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `circle_graph_plots` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/circle_coverage_plot.done` exists and `circle_graph_plots` can proceed without re-running circle coverage plot.
