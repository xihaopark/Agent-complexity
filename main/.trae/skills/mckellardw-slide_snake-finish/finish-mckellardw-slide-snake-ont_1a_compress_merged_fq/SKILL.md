---
name: finish-mckellardw-slide-snake-ont_1a_compress_merged_fq
description: Use this skill when orchestrating the retained "ont_1a_compress_merged_fq" step of the mckellardw slide_snake finish finish workflow. It keeps the ont 1a compress merged fq stage tied to upstream `ont_1a_subset_fastq_by_adapter_type` and the downstream handoff to `ont_1a_split_fastq_to_R1_R2`. It tracks completion via `results/finish/ont_1a_compress_merged_fq.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ont_1a_compress_merged_fq
  step_name: ont 1a compress merged fq
---

# Scope
Use this skill only for the `ont_1a_compress_merged_fq` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ont_1a_subset_fastq_by_adapter_type`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ont_1a_compress_merged_fq.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ont_1a_compress_merged_fq.done`
- Representative outputs: `results/finish/ont_1a_compress_merged_fq.done`
- Execution targets: `ont_1a_compress_merged_fq`
- Downstream handoff: `ont_1a_split_fastq_to_R1_R2`

## Guardrails
- Treat `results/finish/ont_1a_compress_merged_fq.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ont_1a_compress_merged_fq.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ont_1a_split_fastq_to_R1_R2` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ont_1a_compress_merged_fq.done` exists and `ont_1a_split_fastq_to_R1_R2` can proceed without re-running ont 1a compress merged fq.
