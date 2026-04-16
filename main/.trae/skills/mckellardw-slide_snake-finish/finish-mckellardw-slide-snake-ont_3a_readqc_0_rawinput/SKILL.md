---
name: finish-mckellardw-slide-snake-ont_3a_readqc_0_rawinput
description: Use this skill when orchestrating the retained "ont_3a_readQC_0_rawInput" step of the mckellardw slide_snake finish finish workflow. It keeps the ont 3a readQC 0 rawInput stage tied to upstream `ont_2e_cache_seurat` and the downstream handoff to `ont_3a_readQC_1_preCutadapt`. It tracks completion via `results/finish/ont_3a_readQC_0_rawInput.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ont_3a_readQC_0_rawInput
  step_name: ont 3a readQC 0 rawInput
---

# Scope
Use this skill only for the `ont_3a_readQC_0_rawInput` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ont_2e_cache_seurat`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ont_3a_readQC_0_rawInput.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ont_3a_readQC_0_rawInput.done`
- Representative outputs: `results/finish/ont_3a_readQC_0_rawInput.done`
- Execution targets: `ont_3a_readQC_0_rawInput`
- Downstream handoff: `ont_3a_readQC_1_preCutadapt`

## Guardrails
- Treat `results/finish/ont_3a_readQC_0_rawInput.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ont_3a_readQC_0_rawInput.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ont_3a_readQC_1_preCutadapt` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ont_3a_readQC_0_rawInput.done` exists and `ont_3a_readQC_1_preCutadapt` can proceed without re-running ont 3a readQC 0 rawInput.
