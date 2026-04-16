---
name: finish-snakemake-workflows-single-cell-drop-seq-extract_reads_expression
description: Use this skill when orchestrating the retained "extract_reads_expression" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the extract reads expression stage tied to upstream `extract_umi_expression` and the downstream handoff to `SingleCellRnaSeqMetricsCollector`. It tracks completion via `results/finish/extract_reads_expression.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: extract_reads_expression
  step_name: extract reads expression
---

# Scope
Use this skill only for the `extract_reads_expression` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `extract_umi_expression`
- Step file: `finish/single-cell-drop-seq-finish/steps/extract_reads_expression.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/extract_reads_expression.done`
- Representative outputs: `results/finish/extract_reads_expression.done`
- Execution targets: `extract_reads_expression`
- Downstream handoff: `SingleCellRnaSeqMetricsCollector`

## Guardrails
- Treat `results/finish/extract_reads_expression.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/extract_reads_expression.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `SingleCellRnaSeqMetricsCollector` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/extract_reads_expression.done` exists and `SingleCellRnaSeqMetricsCollector` can proceed without re-running extract reads expression.
