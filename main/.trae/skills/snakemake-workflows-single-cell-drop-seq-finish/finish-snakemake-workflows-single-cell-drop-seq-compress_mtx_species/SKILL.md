---
name: finish-snakemake-workflows-single-cell-drop-seq-compress_mtx_species
description: Use this skill when orchestrating the retained "compress_mtx_species" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the compress mtx species stage tied to upstream `convert_long_to_mtx_species` and the downstream handoff to `SingleCellRnaSeqMetricsCollector_species`. It tracks completion via `results/finish/compress_mtx_species.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: compress_mtx_species
  step_name: compress mtx species
---

# Scope
Use this skill only for the `compress_mtx_species` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `convert_long_to_mtx_species`
- Step file: `finish/single-cell-drop-seq-finish/steps/compress_mtx_species.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/compress_mtx_species.done`
- Representative outputs: `results/finish/compress_mtx_species.done`
- Execution targets: `compress_mtx_species`
- Downstream handoff: `SingleCellRnaSeqMetricsCollector_species`

## Guardrails
- Treat `results/finish/compress_mtx_species.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/compress_mtx_species.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `SingleCellRnaSeqMetricsCollector_species` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/compress_mtx_species.done` exists and `SingleCellRnaSeqMetricsCollector_species` can proceed without re-running compress mtx species.
