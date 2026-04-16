---
name: finish-mckellardw-slide-snake-ilmn_2a_build_rrna_gtf
description: Use this skill when orchestrating the retained "ilmn_2a_build_rRNA_gtf" step of the mckellardw slide_snake finish finish workflow. It keeps the ilmn 2a build rRNA gtf stage tied to upstream `ilmn_2a_extract_rRNA_fasta` and the downstream handoff to `ilmn_2a_build_rRNA_bwa_index`. It tracks completion via `results/finish/ilmn_2a_build_rRNA_gtf.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ilmn_2a_build_rRNA_gtf
  step_name: ilmn 2a build rRNA gtf
---

# Scope
Use this skill only for the `ilmn_2a_build_rRNA_gtf` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ilmn_2a_extract_rRNA_fasta`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ilmn_2a_build_rRNA_gtf.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ilmn_2a_build_rRNA_gtf.done`
- Representative outputs: `results/finish/ilmn_2a_build_rRNA_gtf.done`
- Execution targets: `ilmn_2a_build_rRNA_gtf`
- Downstream handoff: `ilmn_2a_build_rRNA_bwa_index`

## Guardrails
- Treat `results/finish/ilmn_2a_build_rRNA_gtf.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ilmn_2a_build_rRNA_gtf.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ilmn_2a_build_rRNA_bwa_index` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ilmn_2a_build_rRNA_gtf.done` exists and `ilmn_2a_build_rRNA_bwa_index` can proceed without re-running ilmn 2a build rRNA gtf.
