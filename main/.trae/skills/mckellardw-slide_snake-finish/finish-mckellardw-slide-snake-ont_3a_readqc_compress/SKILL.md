---
name: finish-mckellardw-slide-snake-ont_3a_readqc_compress
description: Use this skill when orchestrating the retained "ont_3a_readQC_compress" step of the mckellardw slide_snake finish finish workflow. It keeps the ont 3a readQC compress stage tied to upstream `ont_3a_readQC_summaryplot` and the downstream handoff to `ont_3b_qualimap`. It tracks completion via `results/finish/ont_3a_readQC_compress.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ont_3a_readQC_compress
  step_name: ont 3a readQC compress
---

# Scope
Use this skill only for the `ont_3a_readQC_compress` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ont_3a_readQC_summaryplot`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ont_3a_readQC_compress.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ont_3a_readQC_compress.done`
- Representative outputs: `results/finish/ont_3a_readQC_compress.done`
- Execution targets: `ont_3a_readQC_compress`
- Downstream handoff: `ont_3b_qualimap`

## Guardrails
- Treat `results/finish/ont_3a_readQC_compress.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ont_3a_readQC_compress.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ont_3b_qualimap` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ont_3a_readQC_compress.done` exists and `ont_3b_qualimap` can proceed without re-running ont 3a readQC compress.
