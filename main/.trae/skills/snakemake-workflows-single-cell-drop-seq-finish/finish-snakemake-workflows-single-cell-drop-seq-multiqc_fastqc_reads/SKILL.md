---
name: finish-snakemake-workflows-single-cell-drop-seq-multiqc_fastqc_reads
description: Use this skill when orchestrating the retained "multiqc_fastqc_reads" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the multiqc fastqc reads stage tied to upstream `multiqc_fastqc_barcodes` and the downstream handoff to `fasta_fastq_adapter`. It tracks completion via `results/finish/multiqc_fastqc_reads.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: multiqc_fastqc_reads
  step_name: multiqc fastqc reads
---

# Scope
Use this skill only for the `multiqc_fastqc_reads` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `multiqc_fastqc_barcodes`
- Step file: `finish/single-cell-drop-seq-finish/steps/multiqc_fastqc_reads.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/multiqc_fastqc_reads.done`
- Representative outputs: `results/finish/multiqc_fastqc_reads.done`
- Execution targets: `multiqc_fastqc_reads`
- Downstream handoff: `fasta_fastq_adapter`

## Guardrails
- Treat `results/finish/multiqc_fastqc_reads.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/multiqc_fastqc_reads.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `fasta_fastq_adapter` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/multiqc_fastqc_reads.done` exists and `fasta_fastq_adapter` can proceed without re-running multiqc fastqc reads.
