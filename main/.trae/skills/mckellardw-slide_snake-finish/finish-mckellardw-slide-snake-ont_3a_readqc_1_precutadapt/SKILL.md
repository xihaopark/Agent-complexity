---
name: finish-mckellardw-slide-snake-ont_3a_readqc_1_precutadapt
description: Use this skill when orchestrating the retained "ont_3a_readQC_1_preCutadapt" step of the mckellardw slide_snake finish finish workflow. It keeps the ont 3a readQC 1 preCutadapt stage tied to upstream `ont_3a_readQC_0_rawInput` and the downstream handoff to `ont_3a_readQC_2_postCutadapt`. It tracks completion via `results/finish/ont_3a_readQC_1_preCutadapt.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ont_3a_readQC_1_preCutadapt
  step_name: ont 3a readQC 1 preCutadapt
---

# Scope
Use this skill only for the `ont_3a_readQC_1_preCutadapt` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ont_3a_readQC_0_rawInput`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ont_3a_readQC_1_preCutadapt.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ont_3a_readQC_1_preCutadapt.done`
- Representative outputs: `results/finish/ont_3a_readQC_1_preCutadapt.done`
- Execution targets: `ont_3a_readQC_1_preCutadapt`
- Downstream handoff: `ont_3a_readQC_2_postCutadapt`

## Guardrails
- Treat `results/finish/ont_3a_readQC_1_preCutadapt.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ont_3a_readQC_1_preCutadapt.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ont_3a_readQC_2_postCutadapt` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ont_3a_readQC_1_preCutadapt.done` exists and `ont_3a_readQC_2_postCutadapt` can proceed without re-running ont 3a readQC 1 preCutadapt.
