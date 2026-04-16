---
name: finish-mckellardw-slide-snake-ont_1a_merge_formats
description: Use this skill when orchestrating the retained "ont_1a_merge_formats" step of the mckellardw slide_snake finish finish workflow. It keeps the ont 1a merge formats stage tied to upstream `ilmn_7b_readQC_compress` and the downstream handoff to `ont_1a_call_adapter_scan`. It tracks completion via `results/finish/ont_1a_merge_formats.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ont_1a_merge_formats
  step_name: ont 1a merge formats
---

# Scope
Use this skill only for the `ont_1a_merge_formats` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ilmn_7b_readQC_compress`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ont_1a_merge_formats.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ont_1a_merge_formats.done`
- Representative outputs: `results/finish/ont_1a_merge_formats.done`
- Execution targets: `ont_1a_merge_formats`
- Downstream handoff: `ont_1a_call_adapter_scan`

## Guardrails
- Treat `results/finish/ont_1a_merge_formats.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ont_1a_merge_formats.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ont_1a_call_adapter_scan` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ont_1a_merge_formats.done` exists and `ont_1a_call_adapter_scan` can proceed without re-running ont 1a merge formats.
