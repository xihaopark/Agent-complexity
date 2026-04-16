---
name: finish-mckellardw-slide-snake-ont_1a_split_fastq_to_r1_r2
description: Use this skill when orchestrating the retained "ont_1a_split_fastq_to_R1_R2" step of the mckellardw slide_snake finish finish workflow. It keeps the ont 1a split fastq to R1 R2 stage tied to upstream `ont_1a_compress_merged_fq` and the downstream handoff to `ont_1b_cutadapt`. It tracks completion via `results/finish/ont_1a_split_fastq_to_R1_R2.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ont_1a_split_fastq_to_R1_R2
  step_name: ont 1a split fastq to R1 R2
---

# Scope
Use this skill only for the `ont_1a_split_fastq_to_R1_R2` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ont_1a_compress_merged_fq`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ont_1a_split_fastq_to_R1_R2.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ont_1a_split_fastq_to_R1_R2.done`
- Representative outputs: `results/finish/ont_1a_split_fastq_to_R1_R2.done`
- Execution targets: `ont_1a_split_fastq_to_R1_R2`
- Downstream handoff: `ont_1b_cutadapt`

## Guardrails
- Treat `results/finish/ont_1a_split_fastq_to_R1_R2.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ont_1a_split_fastq_to_R1_R2.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ont_1b_cutadapt` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ont_1a_split_fastq_to_R1_R2.done` exists and `ont_1b_cutadapt` can proceed without re-running ont 1a split fastq to R1 R2.
