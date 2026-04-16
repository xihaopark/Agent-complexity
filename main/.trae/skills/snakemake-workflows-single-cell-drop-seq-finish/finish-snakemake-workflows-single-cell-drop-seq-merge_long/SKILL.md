---
name: finish-snakemake-workflows-single-cell-drop-seq-merge_long
description: Use this skill when orchestrating the retained "merge_long" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the merge long stage tied to upstream `plot_rna_metrics_species` and the downstream handoff to `violine_plots`. It tracks completion via `results/finish/merge_long.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: merge_long
  step_name: merge long
---

# Scope
Use this skill only for the `merge_long` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `plot_rna_metrics_species`
- Step file: `finish/single-cell-drop-seq-finish/steps/merge_long.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/merge_long.done`
- Representative outputs: `results/finish/merge_long.done`
- Execution targets: `merge_long`
- Downstream handoff: `violine_plots`

## Guardrails
- Treat `results/finish/merge_long.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/merge_long.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `violine_plots` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/merge_long.done` exists and `violine_plots` can proceed without re-running merge long.
