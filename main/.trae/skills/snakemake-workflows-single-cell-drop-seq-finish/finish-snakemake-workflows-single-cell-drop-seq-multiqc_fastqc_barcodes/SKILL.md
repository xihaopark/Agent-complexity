---
name: finish-snakemake-workflows-single-cell-drop-seq-multiqc_fastqc_barcodes
description: Use this skill when orchestrating the retained "multiqc_fastqc_barcodes" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the multiqc fastqc barcodes stage tied to upstream `fastqc_reads` and the downstream handoff to `multiqc_fastqc_reads`. It tracks completion via `results/finish/multiqc_fastqc_barcodes.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: multiqc_fastqc_barcodes
  step_name: multiqc fastqc barcodes
---

# Scope
Use this skill only for the `multiqc_fastqc_barcodes` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `fastqc_reads`
- Step file: `finish/single-cell-drop-seq-finish/steps/multiqc_fastqc_barcodes.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/multiqc_fastqc_barcodes.done`
- Representative outputs: `results/finish/multiqc_fastqc_barcodes.done`
- Execution targets: `multiqc_fastqc_barcodes`
- Downstream handoff: `multiqc_fastqc_reads`

## Guardrails
- Treat `results/finish/multiqc_fastqc_barcodes.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/multiqc_fastqc_barcodes.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `multiqc_fastqc_reads` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/multiqc_fastqc_barcodes.done` exists and `multiqc_fastqc_reads` can proceed without re-running multiqc fastqc barcodes.
