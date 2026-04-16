---
name: finish-snakemake-workflows-single-cell-drop-seq-plot_rna_metrics_species
description: Use this skill when orchestrating the retained "plot_rna_metrics_species" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the plot rna metrics species stage tied to upstream `SingleCellRnaSeqMetricsCollector_species` and the downstream handoff to `merge_long`. It tracks completion via `results/finish/plot_rna_metrics_species.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: plot_rna_metrics_species
  step_name: plot rna metrics species
---

# Scope
Use this skill only for the `plot_rna_metrics_species` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `SingleCellRnaSeqMetricsCollector_species`
- Step file: `finish/single-cell-drop-seq-finish/steps/plot_rna_metrics_species.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plot_rna_metrics_species.done`
- Representative outputs: `results/finish/plot_rna_metrics_species.done`
- Execution targets: `plot_rna_metrics_species`
- Downstream handoff: `merge_long`

## Guardrails
- Treat `results/finish/plot_rna_metrics_species.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plot_rna_metrics_species.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `merge_long` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plot_rna_metrics_species.done` exists and `merge_long` can proceed without re-running plot rna metrics species.
