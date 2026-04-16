---
name: finish-snakemake-workflows-single-cell-drop-seq-fasta_fastq_adapter
description: Use this skill when orchestrating the retained "fasta_fastq_adapter" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the fasta fastq adapter stage tied to upstream `multiqc_fastqc_reads` and the downstream handoff to `cutadapt_R1`. It tracks completion via `results/finish/fasta_fastq_adapter.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: fasta_fastq_adapter
  step_name: fasta fastq adapter
---

# Scope
Use this skill only for the `fasta_fastq_adapter` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `multiqc_fastqc_reads`
- Step file: `finish/single-cell-drop-seq-finish/steps/fasta_fastq_adapter.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/fasta_fastq_adapter.done`
- Representative outputs: `results/finish/fasta_fastq_adapter.done`
- Execution targets: `fasta_fastq_adapter`
- Downstream handoff: `cutadapt_R1`

## Guardrails
- Treat `results/finish/fasta_fastq_adapter.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/fasta_fastq_adapter.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `cutadapt_R1` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/fasta_fastq_adapter.done` exists and `cutadapt_R1` can proceed without re-running fasta fastq adapter.
