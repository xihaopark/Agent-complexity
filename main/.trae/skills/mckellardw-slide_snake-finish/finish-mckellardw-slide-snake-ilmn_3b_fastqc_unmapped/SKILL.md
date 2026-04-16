---
name: finish-mckellardw-slide-snake-ilmn_3b_fastqc_unmapped
description: Use this skill when orchestrating the retained "ilmn_3b_fastqc_unmapped" step of the mckellardw slide_snake finish finish workflow. It keeps the ilmn 3b fastqc unmapped stage tied to upstream `ilmn_3a_cache_h5ad_STAR` and the downstream handoff to `ilmn_3c_strand_split_bam`. It tracks completion via `results/finish/ilmn_3b_fastqc_unmapped.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ilmn_3b_fastqc_unmapped
  step_name: ilmn 3b fastqc unmapped
---

# Scope
Use this skill only for the `ilmn_3b_fastqc_unmapped` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ilmn_3a_cache_h5ad_STAR`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ilmn_3b_fastqc_unmapped.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ilmn_3b_fastqc_unmapped.done`
- Representative outputs: `results/finish/ilmn_3b_fastqc_unmapped.done`
- Execution targets: `ilmn_3b_fastqc_unmapped`
- Downstream handoff: `ilmn_3c_strand_split_bam`

## Guardrails
- Treat `results/finish/ilmn_3b_fastqc_unmapped.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ilmn_3b_fastqc_unmapped.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ilmn_3c_strand_split_bam` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ilmn_3b_fastqc_unmapped.done` exists and `ilmn_3c_strand_split_bam` can proceed without re-running ilmn 3b fastqc unmapped.
