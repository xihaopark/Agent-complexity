---
name: finish-mckellardw-slide-snake-ont_3a_readqc_3_bam
description: Use this skill when orchestrating the retained "ont_3a_readQC_3_bam" step of the mckellardw slide_snake finish finish workflow. It keeps the ont 3a readQC 3 bam stage tied to upstream `ont_3a_readQC_2_postCutadapt` and the downstream handoff to `ont_3a_readQC_downsample`. It tracks completion via `results/finish/ont_3a_readQC_3_bam.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ont_3a_readQC_3_bam
  step_name: ont 3a readQC 3 bam
---

# Scope
Use this skill only for the `ont_3a_readQC_3_bam` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ont_3a_readQC_2_postCutadapt`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ont_3a_readQC_3_bam.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ont_3a_readQC_3_bam.done`
- Representative outputs: `results/finish/ont_3a_readQC_3_bam.done`
- Execution targets: `ont_3a_readQC_3_bam`
- Downstream handoff: `ont_3a_readQC_downsample`

## Guardrails
- Treat `results/finish/ont_3a_readQC_3_bam.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ont_3a_readQC_3_bam.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ont_3a_readQC_downsample` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ont_3a_readQC_3_bam.done` exists and `ont_3a_readQC_downsample` can proceed without re-running ont 3a readQC 3 bam.
