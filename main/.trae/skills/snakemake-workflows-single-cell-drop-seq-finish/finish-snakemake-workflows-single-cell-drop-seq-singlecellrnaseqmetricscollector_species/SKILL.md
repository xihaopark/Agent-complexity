---
name: finish-snakemake-workflows-single-cell-drop-seq-singlecellrnaseqmetricscollector_species
description: Use this skill when orchestrating the retained "SingleCellRnaSeqMetricsCollector_species" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the SingleCellRnaSeqMetricsCollector species stage tied to upstream `compress_mtx_species` and the downstream handoff to `plot_rna_metrics_species`. It tracks completion via `results/finish/SingleCellRnaSeqMetricsCollector_species.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: SingleCellRnaSeqMetricsCollector_species
  step_name: SingleCellRnaSeqMetricsCollector species
---

# Scope
Use this skill only for the `SingleCellRnaSeqMetricsCollector_species` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `compress_mtx_species`
- Step file: `finish/single-cell-drop-seq-finish/steps/SingleCellRnaSeqMetricsCollector_species.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/SingleCellRnaSeqMetricsCollector_species.done`
- Representative outputs: `results/finish/SingleCellRnaSeqMetricsCollector_species.done`
- Execution targets: `SingleCellRnaSeqMetricsCollector_species`
- Downstream handoff: `plot_rna_metrics_species`

## Guardrails
- Treat `results/finish/SingleCellRnaSeqMetricsCollector_species.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/SingleCellRnaSeqMetricsCollector_species.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plot_rna_metrics_species` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/SingleCellRnaSeqMetricsCollector_species.done` exists and `plot_rna_metrics_species` can proceed without re-running SingleCellRnaSeqMetricsCollector species.
