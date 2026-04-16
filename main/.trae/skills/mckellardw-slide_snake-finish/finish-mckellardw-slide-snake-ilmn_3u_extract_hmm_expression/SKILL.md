---
name: finish-mckellardw-slide-snake-ilmn_3u_extract_hmm_expression
description: Use this skill when orchestrating the retained "ilmn_3u_extract_HMM_expression" step of the mckellardw slide_snake finish finish workflow. It keeps the ilmn 3u extract HMM expression stage tied to upstream `ilmn_3u_sort_index_tagged_bam` and the downstream handoff to `ilmn_3u_counts_long2mtx`. It tracks completion via `results/finish/ilmn_3u_extract_HMM_expression.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ilmn_3u_extract_HMM_expression
  step_name: ilmn 3u extract HMM expression
---

# Scope
Use this skill only for the `ilmn_3u_extract_HMM_expression` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ilmn_3u_sort_index_tagged_bam`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ilmn_3u_extract_HMM_expression.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ilmn_3u_extract_HMM_expression.done`
- Representative outputs: `results/finish/ilmn_3u_extract_HMM_expression.done`
- Execution targets: `ilmn_3u_extract_HMM_expression`
- Downstream handoff: `ilmn_3u_counts_long2mtx`

## Guardrails
- Treat `results/finish/ilmn_3u_extract_HMM_expression.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ilmn_3u_extract_HMM_expression.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ilmn_3u_counts_long2mtx` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ilmn_3u_extract_HMM_expression.done` exists and `ilmn_3u_counts_long2mtx` can proceed without re-running ilmn 3u extract HMM expression.
