---
name: finish-snakemake-workflows-cyrcular-calling-copy_qc_plots_for_datavzrd
description: Use this skill when orchestrating the retained "copy_qc_plots_for_datavzrd" step of the snakemake workflows cyrcular calling finish finish workflow. It keeps the copy qc plots for datavzrd stage tied to upstream `render_datavzrd_config` and the downstream handoff to `copy_graph_plots_for_datavzrd`. It tracks completion via `results/finish/copy_qc_plots_for_datavzrd.done`.
metadata:
  workflow_id: cyrcular-calling-finish
  workflow_name: snakemake workflows cyrcular calling finish
  step_id: copy_qc_plots_for_datavzrd
  step_name: copy qc plots for datavzrd
---

# Scope
Use this skill only for the `copy_qc_plots_for_datavzrd` step in `cyrcular-calling-finish`.

## Orchestration
- Upstream requirements: `render_datavzrd_config`
- Step file: `finish/cyrcular-calling-finish/steps/copy_qc_plots_for_datavzrd.smk`
- Config file: `finish/cyrcular-calling-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/copy_qc_plots_for_datavzrd.done`
- Representative outputs: `results/finish/copy_qc_plots_for_datavzrd.done`
- Execution targets: `copy_qc_plots_for_datavzrd`
- Downstream handoff: `copy_graph_plots_for_datavzrd`

## Guardrails
- Treat `results/finish/copy_qc_plots_for_datavzrd.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/copy_qc_plots_for_datavzrd.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `copy_graph_plots_for_datavzrd` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/copy_qc_plots_for_datavzrd.done` exists and `copy_graph_plots_for_datavzrd` can proceed without re-running copy qc plots for datavzrd.
