---
name: finish-mckellardw-slide-snake-ilmn_2a_bwa_rrna_filtered_fastqc
description: Use this skill when orchestrating the retained "ilmn_2a_bwa_rRNA_filtered_fastqc" step of the mckellardw slide_snake finish finish workflow. It keeps the ilmn 2a bwa rRNA filtered fastqc stage tied to upstream `ilmn_2a_bwa_rRNA_compress_unmapped` and the downstream handoff to `ilmn_2b_ribodetector`. It tracks completion via `results/finish/ilmn_2a_bwa_rRNA_filtered_fastqc.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ilmn_2a_bwa_rRNA_filtered_fastqc
  step_name: ilmn 2a bwa rRNA filtered fastqc
---

# Scope
Use this skill only for the `ilmn_2a_bwa_rRNA_filtered_fastqc` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ilmn_2a_bwa_rRNA_compress_unmapped`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ilmn_2a_bwa_rRNA_filtered_fastqc.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ilmn_2a_bwa_rRNA_filtered_fastqc.done`
- Representative outputs: `results/finish/ilmn_2a_bwa_rRNA_filtered_fastqc.done`
- Execution targets: `ilmn_2a_bwa_rRNA_filtered_fastqc`
- Downstream handoff: `ilmn_2b_ribodetector`

## Guardrails
- Treat `results/finish/ilmn_2a_bwa_rRNA_filtered_fastqc.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ilmn_2a_bwa_rRNA_filtered_fastqc.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ilmn_2b_ribodetector` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ilmn_2a_bwa_rRNA_filtered_fastqc.done` exists and `ilmn_2b_ribodetector` can proceed without re-running ilmn 2a bwa rRNA filtered fastqc.
