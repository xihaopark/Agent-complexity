---
name: finish-mckellardw-slide-snake-ilmn_2a_build_rrna_bwa_index
description: Use this skill when orchestrating the retained "ilmn_2a_build_rRNA_bwa_index" step of the mckellardw slide_snake finish finish workflow. It keeps the ilmn 2a build rRNA bwa index stage tied to upstream `ilmn_2a_build_rRNA_gtf` and the downstream handoff to `ilmn_2a_bwa_rRNA_align`. It tracks completion via `results/finish/ilmn_2a_build_rRNA_bwa_index.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ilmn_2a_build_rRNA_bwa_index
  step_name: ilmn 2a build rRNA bwa index
---

# Scope
Use this skill only for the `ilmn_2a_build_rRNA_bwa_index` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ilmn_2a_build_rRNA_gtf`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ilmn_2a_build_rRNA_bwa_index.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ilmn_2a_build_rRNA_bwa_index.done`
- Representative outputs: `results/finish/ilmn_2a_build_rRNA_bwa_index.done`
- Execution targets: `ilmn_2a_build_rRNA_bwa_index`
- Downstream handoff: `ilmn_2a_bwa_rRNA_align`

## Guardrails
- Treat `results/finish/ilmn_2a_build_rRNA_bwa_index.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ilmn_2a_build_rRNA_bwa_index.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ilmn_2a_bwa_rRNA_align` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ilmn_2a_build_rRNA_bwa_index.done` exists and `ilmn_2a_bwa_rRNA_align` can proceed without re-running ilmn 2a build rRNA bwa index.
