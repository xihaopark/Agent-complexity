---
name: finish-mckellardw-slide-snake-ont_3a_readqc_2_postcutadapt
description: Use this skill when orchestrating the retained "ont_3a_readQC_2_postCutadapt" step of the mckellardw slide_snake finish finish workflow. It keeps the ont 3a readQC 2 postCutadapt stage tied to upstream `ont_3a_readQC_1_preCutadapt` and the downstream handoff to `ont_3a_readQC_3_bam`. It tracks completion via `results/finish/ont_3a_readQC_2_postCutadapt.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ont_3a_readQC_2_postCutadapt
  step_name: ont 3a readQC 2 postCutadapt
---

# Scope
Use this skill only for the `ont_3a_readQC_2_postCutadapt` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ont_3a_readQC_1_preCutadapt`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ont_3a_readQC_2_postCutadapt.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ont_3a_readQC_2_postCutadapt.done`
- Representative outputs: `results/finish/ont_3a_readQC_2_postCutadapt.done`
- Execution targets: `ont_3a_readQC_2_postCutadapt`
- Downstream handoff: `ont_3a_readQC_3_bam`

## Guardrails
- Treat `results/finish/ont_3a_readQC_2_postCutadapt.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ont_3a_readQC_2_postCutadapt.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ont_3a_readQC_3_bam` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ont_3a_readQC_2_postCutadapt.done` exists and `ont_3a_readQC_3_bam` can proceed without re-running ont 3a readQC 2 postCutadapt.
