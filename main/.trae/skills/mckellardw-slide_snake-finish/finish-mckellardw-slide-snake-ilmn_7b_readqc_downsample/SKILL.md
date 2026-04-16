---
name: finish-mckellardw-slide-snake-ilmn_7b_readqc_downsample
description: Use this skill when orchestrating the retained "ilmn_7b_readQC_downsample" step of the mckellardw slide_snake finish finish workflow. It keeps the ilmn 7b readQC downsample stage tied to upstream `ilmn_7b_readQC_3_bam` and the downstream handoff to `ilmn_7b_readQC_summaryplot`. It tracks completion via `results/finish/ilmn_7b_readQC_downsample.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ilmn_7b_readQC_downsample
  step_name: ilmn 7b readQC downsample
---

# Scope
Use this skill only for the `ilmn_7b_readQC_downsample` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ilmn_7b_readQC_3_bam`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ilmn_7b_readQC_downsample.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ilmn_7b_readQC_downsample.done`
- Representative outputs: `results/finish/ilmn_7b_readQC_downsample.done`
- Execution targets: `ilmn_7b_readQC_downsample`
- Downstream handoff: `ilmn_7b_readQC_summaryplot`

## Guardrails
- Treat `results/finish/ilmn_7b_readQC_downsample.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ilmn_7b_readQC_downsample.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ilmn_7b_readQC_summaryplot` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ilmn_7b_readQC_downsample.done` exists and `ilmn_7b_readQC_summaryplot` can proceed without re-running ilmn 7b readQC downsample.
