---
name: finish-mckellardw-slide-snake-ilmn_7b_readqc_summaryplot
description: Use this skill when orchestrating the retained "ilmn_7b_readQC_summaryplot" step of the mckellardw slide_snake finish finish workflow. It keeps the ilmn 7b readQC summaryplot stage tied to upstream `ilmn_7b_readQC_downsample` and the downstream handoff to `ilmn_7b_readQC_compress`. It tracks completion via `results/finish/ilmn_7b_readQC_summaryplot.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ilmn_7b_readQC_summaryplot
  step_name: ilmn 7b readQC summaryplot
---

# Scope
Use this skill only for the `ilmn_7b_readQC_summaryplot` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ilmn_7b_readQC_downsample`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ilmn_7b_readQC_summaryplot.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ilmn_7b_readQC_summaryplot.done`
- Representative outputs: `results/finish/ilmn_7b_readQC_summaryplot.done`
- Execution targets: `ilmn_7b_readQC_summaryplot`
- Downstream handoff: `ilmn_7b_readQC_compress`

## Guardrails
- Treat `results/finish/ilmn_7b_readQC_summaryplot.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ilmn_7b_readQC_summaryplot.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ilmn_7b_readQC_compress` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ilmn_7b_readQC_summaryplot.done` exists and `ilmn_7b_readQC_compress` can proceed without re-running ilmn 7b readQC summaryplot.
