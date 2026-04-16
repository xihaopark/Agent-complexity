---
name: finish-mckellardw-slide-snake-ilmn_2a_bwa_rrna_compress_unmapped
description: Use this skill when orchestrating the retained "ilmn_2a_bwa_rRNA_compress_unmapped" step of the mckellardw slide_snake finish finish workflow. It keeps the ilmn 2a bwa rRNA compress unmapped stage tied to upstream `ilmn_2a_bwa_rRNA_filter_trimmed_R1` and the downstream handoff to `ilmn_2a_bwa_rRNA_filtered_fastqc`. It tracks completion via `results/finish/ilmn_2a_bwa_rRNA_compress_unmapped.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ilmn_2a_bwa_rRNA_compress_unmapped
  step_name: ilmn 2a bwa rRNA compress unmapped
---

# Scope
Use this skill only for the `ilmn_2a_bwa_rRNA_compress_unmapped` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ilmn_2a_bwa_rRNA_filter_trimmed_R1`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ilmn_2a_bwa_rRNA_compress_unmapped.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ilmn_2a_bwa_rRNA_compress_unmapped.done`
- Representative outputs: `results/finish/ilmn_2a_bwa_rRNA_compress_unmapped.done`
- Execution targets: `ilmn_2a_bwa_rRNA_compress_unmapped`
- Downstream handoff: `ilmn_2a_bwa_rRNA_filtered_fastqc`

## Guardrails
- Treat `results/finish/ilmn_2a_bwa_rRNA_compress_unmapped.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ilmn_2a_bwa_rRNA_compress_unmapped.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ilmn_2a_bwa_rRNA_filtered_fastqc` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ilmn_2a_bwa_rRNA_compress_unmapped.done` exists and `ilmn_2a_bwa_rRNA_filtered_fastqc` can proceed without re-running ilmn 2a bwa rRNA compress unmapped.
