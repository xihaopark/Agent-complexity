---
name: finish-mckellardw-slide-snake-ilmn_2a_extract_rrna_fasta
description: Use this skill when orchestrating the retained "ilmn_2a_extract_rRNA_fasta" step of the mckellardw slide_snake finish finish workflow. It keeps the ilmn 2a extract rRNA fasta stage tied to upstream `ilmn_1c_summarize_bc_correction` and the downstream handoff to `ilmn_2a_build_rRNA_gtf`. It tracks completion via `results/finish/ilmn_2a_extract_rRNA_fasta.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ilmn_2a_extract_rRNA_fasta
  step_name: ilmn 2a extract rRNA fasta
---

# Scope
Use this skill only for the `ilmn_2a_extract_rRNA_fasta` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ilmn_1c_summarize_bc_correction`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ilmn_2a_extract_rRNA_fasta.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ilmn_2a_extract_rRNA_fasta.done`
- Representative outputs: `results/finish/ilmn_2a_extract_rRNA_fasta.done`
- Execution targets: `ilmn_2a_extract_rRNA_fasta`
- Downstream handoff: `ilmn_2a_build_rRNA_gtf`

## Guardrails
- Treat `results/finish/ilmn_2a_extract_rRNA_fasta.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ilmn_2a_extract_rRNA_fasta.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ilmn_2a_build_rRNA_gtf` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ilmn_2a_extract_rRNA_fasta.done` exists and `ilmn_2a_build_rRNA_gtf` can proceed without re-running ilmn 2a extract rRNA fasta.
