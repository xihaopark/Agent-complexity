---
name: finish-snakemake-workflows-cyrcular-calling-copy_graph_plots_for_datavzrd
description: Use this skill when orchestrating the retained "copy_graph_plots_for_datavzrd" step of the snakemake workflows cyrcular calling finish finish workflow. It keeps the copy graph plots for datavzrd stage tied to upstream `copy_qc_plots_for_datavzrd` and the downstream handoff to `datavzrd_circle_calls`. It tracks completion via `results/finish/copy_graph_plots_for_datavzrd.done`.
metadata:
  workflow_id: cyrcular-calling-finish
  workflow_name: snakemake workflows cyrcular calling finish
  step_id: copy_graph_plots_for_datavzrd
  step_name: copy graph plots for datavzrd
---

# Scope
Use this skill only for the `copy_graph_plots_for_datavzrd` step in `cyrcular-calling-finish`.

## Orchestration
- Upstream requirements: `copy_qc_plots_for_datavzrd`
- Step file: `finish/cyrcular-calling-finish/steps/copy_graph_plots_for_datavzrd.smk`
- Config file: `finish/cyrcular-calling-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/copy_graph_plots_for_datavzrd.done`
- Representative outputs: `results/finish/copy_graph_plots_for_datavzrd.done`
- Execution targets: `copy_graph_plots_for_datavzrd`
- Downstream handoff: `datavzrd_circle_calls`

## Guardrails
- Treat `results/finish/copy_graph_plots_for_datavzrd.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/copy_graph_plots_for_datavzrd.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `datavzrd_circle_calls` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/copy_graph_plots_for_datavzrd.done` exists and `datavzrd_circle_calls` can proceed without re-running copy graph plots for datavzrd.
