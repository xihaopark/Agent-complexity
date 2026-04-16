---
name: finish-snakemake-workflows-single-cell-drop-seq-fastqc_barcodes
description: Use this skill when orchestrating the retained "fastqc_barcodes" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the fastqc barcodes stage tied to upstream `create_star_index` and the downstream handoff to `fastqc_reads`. It tracks completion via `results/finish/fastqc_barcodes.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: fastqc_barcodes
  step_name: fastqc barcodes
---

# Scope
Use this skill only for the `fastqc_barcodes` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `create_star_index`
- Step file: `finish/single-cell-drop-seq-finish/steps/fastqc_barcodes.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/fastqc_barcodes.done`
- Representative outputs: `results/finish/fastqc_barcodes.done`
- Execution targets: `fastqc_barcodes`
- Downstream handoff: `fastqc_reads`

## Guardrails
- Treat `results/finish/fastqc_barcodes.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/fastqc_barcodes.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `fastqc_reads` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/fastqc_barcodes.done` exists and `fastqc_reads` can proceed without re-running fastqc barcodes.
