---
name: finish-snakemake-workflows-cyrcular-calling-datavzrd_circle_calls
description: Use this skill when orchestrating the retained "datavzrd_circle_calls" step of the snakemake workflows cyrcular calling finish finish workflow. It keeps the datavzrd circle calls stage tied to upstream `copy_graph_plots_for_datavzrd` and the downstream handoff to `all`. It tracks completion via `results/finish/datavzrd_circle_calls.done`.
metadata:
  workflow_id: cyrcular-calling-finish
  workflow_name: snakemake workflows cyrcular calling finish
  step_id: datavzrd_circle_calls
  step_name: datavzrd circle calls
---

# Scope
Use this skill only for the `datavzrd_circle_calls` step in `cyrcular-calling-finish`.

## Orchestration
- Upstream requirements: `copy_graph_plots_for_datavzrd`
- Step file: `finish/cyrcular-calling-finish/steps/datavzrd_circle_calls.smk`
- Config file: `finish/cyrcular-calling-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/datavzrd_circle_calls.done`
- Representative outputs: `results/finish/datavzrd_circle_calls.done`
- Execution targets: `datavzrd_circle_calls`
- Downstream handoff: `all`

## Guardrails
- Treat `results/finish/datavzrd_circle_calls.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/datavzrd_circle_calls.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `all` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/datavzrd_circle_calls.done` exists and `all` can proceed without re-running datavzrd circle calls.
