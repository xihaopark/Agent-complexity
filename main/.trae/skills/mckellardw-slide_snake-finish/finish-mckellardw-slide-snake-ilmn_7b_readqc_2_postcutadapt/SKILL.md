---
name: finish-mckellardw-slide-snake-ilmn_7b_readqc_2_postcutadapt
description: Use this skill when orchestrating the retained "ilmn_7b_readQC_2_postCutadapt" step of the mckellardw slide_snake finish finish workflow. It keeps the ilmn 7b readQC 2 postCutadapt stage tied to upstream `ilmn_7b_readQC_1_preCutadapt` and the downstream handoff to `ilmn_7b_readQC_3_twiceCutadapt`. It tracks completion via `results/finish/ilmn_7b_readQC_2_postCutadapt.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ilmn_7b_readQC_2_postCutadapt
  step_name: ilmn 7b readQC 2 postCutadapt
---

# Scope
Use this skill only for the `ilmn_7b_readQC_2_postCutadapt` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ilmn_7b_readQC_1_preCutadapt`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ilmn_7b_readQC_2_postCutadapt.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ilmn_7b_readQC_2_postCutadapt.done`
- Representative outputs: `results/finish/ilmn_7b_readQC_2_postCutadapt.done`
- Execution targets: `ilmn_7b_readQC_2_postCutadapt`
- Downstream handoff: `ilmn_7b_readQC_3_twiceCutadapt`

## Guardrails
- Treat `results/finish/ilmn_7b_readQC_2_postCutadapt.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ilmn_7b_readQC_2_postCutadapt.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ilmn_7b_readQC_3_twiceCutadapt` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ilmn_7b_readQC_2_postCutadapt.done` exists and `ilmn_7b_readQC_3_twiceCutadapt` can proceed without re-running ilmn 7b readQC 2 postCutadapt.
