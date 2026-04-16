---
name: finish-snakemake-workflows-single-cell-drop-seq-fastqc_reads
description: Use this skill when orchestrating the retained "fastqc_reads" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the fastqc reads stage tied to upstream `fastqc_barcodes` and the downstream handoff to `multiqc_fastqc_barcodes`. It tracks completion via `results/finish/fastqc_reads.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: fastqc_reads
  step_name: fastqc reads
---

# Scope
Use this skill only for the `fastqc_reads` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `fastqc_barcodes`
- Step file: `finish/single-cell-drop-seq-finish/steps/fastqc_reads.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/fastqc_reads.done`
- Representative outputs: `results/finish/fastqc_reads.done`
- Execution targets: `fastqc_reads`
- Downstream handoff: `multiqc_fastqc_barcodes`

## Guardrails
- Treat `results/finish/fastqc_reads.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/fastqc_reads.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `multiqc_fastqc_barcodes` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/fastqc_reads.done` exists and `multiqc_fastqc_barcodes` can proceed without re-running fastqc reads.
