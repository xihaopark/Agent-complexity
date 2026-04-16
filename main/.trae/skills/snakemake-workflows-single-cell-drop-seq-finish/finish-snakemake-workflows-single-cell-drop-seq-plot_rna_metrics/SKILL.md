---
name: finish-snakemake-workflows-single-cell-drop-seq-plot_rna_metrics
description: Use this skill when orchestrating the retained "plot_rna_metrics" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the plot rna metrics stage tied to upstream `SingleCellRnaSeqMetricsCollector` and the downstream handoff to `convert_long_to_mtx`. It tracks completion via `results/finish/plot_rna_metrics.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: plot_rna_metrics
  step_name: plot rna metrics
---

# Scope
Use this skill only for the `plot_rna_metrics` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `SingleCellRnaSeqMetricsCollector`
- Step file: `finish/single-cell-drop-seq-finish/steps/plot_rna_metrics.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plot_rna_metrics.done`
- Representative outputs: `results/finish/plot_rna_metrics.done`
- Execution targets: `plot_rna_metrics`
- Downstream handoff: `convert_long_to_mtx`

## Guardrails
- Treat `results/finish/plot_rna_metrics.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plot_rna_metrics.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `convert_long_to_mtx` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plot_rna_metrics.done` exists and `convert_long_to_mtx` can proceed without re-running plot rna metrics.
