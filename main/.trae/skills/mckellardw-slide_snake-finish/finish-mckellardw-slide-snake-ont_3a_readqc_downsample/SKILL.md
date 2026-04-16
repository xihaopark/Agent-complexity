---
name: finish-mckellardw-slide-snake-ont_3a_readqc_downsample
description: Use this skill when orchestrating the retained "ont_3a_readQC_downsample" step of the mckellardw slide_snake finish finish workflow. It keeps the ont 3a readQC downsample stage tied to upstream `ont_3a_readQC_3_bam` and the downstream handoff to `ont_3a_readQC_summaryplot`. It tracks completion via `results/finish/ont_3a_readQC_downsample.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ont_3a_readQC_downsample
  step_name: ont 3a readQC downsample
---

# Scope
Use this skill only for the `ont_3a_readQC_downsample` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ont_3a_readQC_3_bam`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ont_3a_readQC_downsample.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ont_3a_readQC_downsample.done`
- Representative outputs: `results/finish/ont_3a_readQC_downsample.done`
- Execution targets: `ont_3a_readQC_downsample`
- Downstream handoff: `ont_3a_readQC_summaryplot`

## Guardrails
- Treat `results/finish/ont_3a_readQC_downsample.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ont_3a_readQC_downsample.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ont_3a_readQC_summaryplot` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ont_3a_readQC_downsample.done` exists and `ont_3a_readQC_summaryplot` can proceed without re-running ont 3a readQC downsample.
