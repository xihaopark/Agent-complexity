---
name: finish-snakemake-workflows-single-cell-drop-seq-cutadapt_r1
description: Use this skill when orchestrating the retained "cutadapt_R1" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the cutadapt R1 stage tied to upstream `fasta_fastq_adapter` and the downstream handoff to `cutadapt_R2`. It tracks completion via `results/finish/cutadapt_R1.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: cutadapt_R1
  step_name: cutadapt R1
---

# Scope
Use this skill only for the `cutadapt_R1` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `fasta_fastq_adapter`
- Step file: `finish/single-cell-drop-seq-finish/steps/cutadapt_R1.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/cutadapt_R1.done`
- Representative outputs: `results/finish/cutadapt_R1.done`
- Execution targets: `cutadapt_R1`
- Downstream handoff: `cutadapt_R2`

## Guardrails
- Treat `results/finish/cutadapt_R1.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/cutadapt_R1.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `cutadapt_R2` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/cutadapt_R1.done` exists and `cutadapt_R2` can proceed without re-running cutadapt R1.
