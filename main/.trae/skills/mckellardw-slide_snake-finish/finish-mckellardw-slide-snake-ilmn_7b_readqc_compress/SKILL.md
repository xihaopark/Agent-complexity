---
name: finish-mckellardw-slide-snake-ilmn_7b_readqc_compress
description: Use this skill when orchestrating the retained "ilmn_7b_readQC_compress" step of the mckellardw slide_snake finish finish workflow. It keeps the ilmn 7b readQC compress stage tied to upstream `ilmn_7b_readQC_summaryplot` and the downstream handoff to `ont_1a_merge_formats`. It tracks completion via `results/finish/ilmn_7b_readQC_compress.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ilmn_7b_readQC_compress
  step_name: ilmn 7b readQC compress
---

# Scope
Use this skill only for the `ilmn_7b_readQC_compress` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ilmn_7b_readQC_summaryplot`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ilmn_7b_readQC_compress.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ilmn_7b_readQC_compress.done`
- Representative outputs: `results/finish/ilmn_7b_readQC_compress.done`
- Execution targets: `ilmn_7b_readQC_compress`
- Downstream handoff: `ont_1a_merge_formats`

## Guardrails
- Treat `results/finish/ilmn_7b_readQC_compress.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ilmn_7b_readQC_compress.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ont_1a_merge_formats` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ilmn_7b_readQC_compress.done` exists and `ont_1a_merge_formats` can proceed without re-running ilmn 7b readQC compress.
