---
name: finish-snakemake-workflows-single-cell-drop-seq-singlecellrnaseqmetricscollector
description: Use this skill when orchestrating the retained "SingleCellRnaSeqMetricsCollector" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the SingleCellRnaSeqMetricsCollector stage tied to upstream `extract_reads_expression` and the downstream handoff to `plot_rna_metrics`. It tracks completion via `results/finish/SingleCellRnaSeqMetricsCollector.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: SingleCellRnaSeqMetricsCollector
  step_name: SingleCellRnaSeqMetricsCollector
---

# Scope
Use this skill only for the `SingleCellRnaSeqMetricsCollector` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `extract_reads_expression`
- Step file: `finish/single-cell-drop-seq-finish/steps/SingleCellRnaSeqMetricsCollector.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/SingleCellRnaSeqMetricsCollector.done`
- Representative outputs: `results/finish/SingleCellRnaSeqMetricsCollector.done`
- Execution targets: `SingleCellRnaSeqMetricsCollector`
- Downstream handoff: `plot_rna_metrics`

## Guardrails
- Treat `results/finish/SingleCellRnaSeqMetricsCollector.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/SingleCellRnaSeqMetricsCollector.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plot_rna_metrics` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/SingleCellRnaSeqMetricsCollector.done` exists and `plot_rna_metrics` can proceed without re-running SingleCellRnaSeqMetricsCollector.
