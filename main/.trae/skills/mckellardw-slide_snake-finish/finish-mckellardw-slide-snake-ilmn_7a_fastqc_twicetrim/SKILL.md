---
name: finish-mckellardw-slide-snake-ilmn_7a_fastqc_twicetrim
description: Use this skill when orchestrating the retained "ilmn_7a_fastQC_twiceTrim" step of the mckellardw slide_snake finish finish workflow. It keeps the ilmn 7a fastQC twiceTrim stage tied to upstream `ilmn_7a_fastQC_postTrim` and the downstream handoff to `ilmn_7b_readQC_0_rawInput`. It tracks completion via `results/finish/ilmn_7a_fastQC_twiceTrim.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ilmn_7a_fastQC_twiceTrim
  step_name: ilmn 7a fastQC twiceTrim
---

# Scope
Use this skill only for the `ilmn_7a_fastQC_twiceTrim` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ilmn_7a_fastQC_postTrim`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ilmn_7a_fastQC_twiceTrim.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ilmn_7a_fastQC_twiceTrim.done`
- Representative outputs: `results/finish/ilmn_7a_fastQC_twiceTrim.done`
- Execution targets: `ilmn_7a_fastQC_twiceTrim`
- Downstream handoff: `ilmn_7b_readQC_0_rawInput`

## Guardrails
- Treat `results/finish/ilmn_7a_fastQC_twiceTrim.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ilmn_7a_fastQC_twiceTrim.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ilmn_7b_readQC_0_rawInput` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ilmn_7a_fastQC_twiceTrim.done` exists and `ilmn_7b_readQC_0_rawInput` can proceed without re-running ilmn 7a fastQC twiceTrim.
