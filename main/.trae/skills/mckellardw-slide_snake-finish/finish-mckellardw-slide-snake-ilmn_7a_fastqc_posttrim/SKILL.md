---
name: finish-mckellardw-slide-snake-ilmn_7a_fastqc_posttrim
description: Use this skill when orchestrating the retained "ilmn_7a_fastQC_postTrim" step of the mckellardw slide_snake finish finish workflow. It keeps the ilmn 7a fastQC postTrim stage tied to upstream `ilmn_7a_fastQC_preTrim` and the downstream handoff to `ilmn_7a_fastQC_twiceTrim`. It tracks completion via `results/finish/ilmn_7a_fastQC_postTrim.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ilmn_7a_fastQC_postTrim
  step_name: ilmn 7a fastQC postTrim
---

# Scope
Use this skill only for the `ilmn_7a_fastQC_postTrim` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ilmn_7a_fastQC_preTrim`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ilmn_7a_fastQC_postTrim.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ilmn_7a_fastQC_postTrim.done`
- Representative outputs: `results/finish/ilmn_7a_fastQC_postTrim.done`
- Execution targets: `ilmn_7a_fastQC_postTrim`
- Downstream handoff: `ilmn_7a_fastQC_twiceTrim`

## Guardrails
- Treat `results/finish/ilmn_7a_fastQC_postTrim.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ilmn_7a_fastQC_postTrim.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ilmn_7a_fastQC_twiceTrim` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ilmn_7a_fastQC_postTrim.done` exists and `ilmn_7a_fastQC_twiceTrim` can proceed without re-running ilmn 7a fastQC postTrim.
