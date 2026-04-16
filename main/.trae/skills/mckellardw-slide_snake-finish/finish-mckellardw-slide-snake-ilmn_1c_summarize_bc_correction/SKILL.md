---
name: finish-mckellardw-slide-snake-ilmn_1c_summarize_bc_correction
description: Use this skill when orchestrating the retained "ilmn_1c_summarize_bc_correction" step of the mckellardw slide_snake finish finish workflow. It keeps the ilmn 1c summarize bc correction stage tied to upstream `ilmn_1c_tsv_bc_correction` and the downstream handoff to `ilmn_2a_extract_rRNA_fasta`. It tracks completion via `results/finish/ilmn_1c_summarize_bc_correction.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ilmn_1c_summarize_bc_correction
  step_name: ilmn 1c summarize bc correction
---

# Scope
Use this skill only for the `ilmn_1c_summarize_bc_correction` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ilmn_1c_tsv_bc_correction`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ilmn_1c_summarize_bc_correction.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ilmn_1c_summarize_bc_correction.done`
- Representative outputs: `results/finish/ilmn_1c_summarize_bc_correction.done`
- Execution targets: `ilmn_1c_summarize_bc_correction`
- Downstream handoff: `ilmn_2a_extract_rRNA_fasta`

## Guardrails
- Treat `results/finish/ilmn_1c_summarize_bc_correction.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ilmn_1c_summarize_bc_correction.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ilmn_2a_extract_rRNA_fasta` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ilmn_1c_summarize_bc_correction.done` exists and `ilmn_2a_extract_rRNA_fasta` can proceed without re-running ilmn 1c summarize bc correction.
