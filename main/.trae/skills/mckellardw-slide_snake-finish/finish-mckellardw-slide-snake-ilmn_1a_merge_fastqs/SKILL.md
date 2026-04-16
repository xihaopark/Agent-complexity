---
name: finish-mckellardw-slide-snake-ilmn_1a_merge_fastqs
description: Use this skill when orchestrating the retained "ilmn_1a_merge_fastqs" step of the mckellardw slide_snake finish finish workflow. It keeps the ilmn 1a merge fastqs stage tied to upstream `BC_write_whitelist_variants` and the downstream handoff to `ilmn_1b_cutadapt`. It tracks completion via `results/finish/ilmn_1a_merge_fastqs.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ilmn_1a_merge_fastqs
  step_name: ilmn 1a merge fastqs
---

# Scope
Use this skill only for the `ilmn_1a_merge_fastqs` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `BC_write_whitelist_variants`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ilmn_1a_merge_fastqs.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ilmn_1a_merge_fastqs.done`
- Representative outputs: `results/finish/ilmn_1a_merge_fastqs.done`
- Execution targets: `ilmn_1a_merge_fastqs`
- Downstream handoff: `ilmn_1b_cutadapt`

## Guardrails
- Treat `results/finish/ilmn_1a_merge_fastqs.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ilmn_1a_merge_fastqs.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ilmn_1b_cutadapt` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ilmn_1a_merge_fastqs.done` exists and `ilmn_1b_cutadapt` can proceed without re-running ilmn 1a merge fastqs.
