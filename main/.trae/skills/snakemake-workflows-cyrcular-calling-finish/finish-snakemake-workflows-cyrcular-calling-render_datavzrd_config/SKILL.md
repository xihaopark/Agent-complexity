---
name: finish-snakemake-workflows-cyrcular-calling-render_datavzrd_config
description: Use this skill when orchestrating the retained "render_datavzrd_config" step of the snakemake workflows cyrcular calling finish finish workflow. It keeps the render datavzrd config stage tied to upstream `circle_graph_plots` and the downstream handoff to `copy_qc_plots_for_datavzrd`. It tracks completion via `results/finish/render_datavzrd_config.done`.
metadata:
  workflow_id: cyrcular-calling-finish
  workflow_name: snakemake workflows cyrcular calling finish
  step_id: render_datavzrd_config
  step_name: render datavzrd config
---

# Scope
Use this skill only for the `render_datavzrd_config` step in `cyrcular-calling-finish`.

## Orchestration
- Upstream requirements: `circle_graph_plots`
- Step file: `finish/cyrcular-calling-finish/steps/render_datavzrd_config.smk`
- Config file: `finish/cyrcular-calling-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/render_datavzrd_config.done`
- Representative outputs: `results/finish/render_datavzrd_config.done`
- Execution targets: `render_datavzrd_config`
- Downstream handoff: `copy_qc_plots_for_datavzrd`

## Guardrails
- Treat `results/finish/render_datavzrd_config.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/render_datavzrd_config.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `copy_qc_plots_for_datavzrd` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/render_datavzrd_config.done` exists and `copy_qc_plots_for_datavzrd` can proceed without re-running render datavzrd config.
