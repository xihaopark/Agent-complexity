---
name: finish-snakemake-workflows-single-cell-drop-seq-violine_plots
description: Use this skill when orchestrating the retained "violine_plots" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the violine plots stage tied to upstream `merge_long` and the downstream handoff to `summary_stats`. It tracks completion via `results/finish/violine_plots.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: violine_plots
  step_name: violine plots
---

# Scope
Use this skill only for the `violine_plots` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `merge_long`
- Step file: `finish/single-cell-drop-seq-finish/steps/violine_plots.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/violine_plots.done`
- Representative outputs: `results/finish/violine_plots.done`
- Execution targets: `violine_plots`
- Downstream handoff: `summary_stats`

## Guardrails
- Treat `results/finish/violine_plots.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/violine_plots.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `summary_stats` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/violine_plots.done` exists and `summary_stats` can proceed without re-running violine plots.
