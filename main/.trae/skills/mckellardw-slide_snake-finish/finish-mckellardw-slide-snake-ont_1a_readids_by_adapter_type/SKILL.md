---
name: finish-mckellardw-slide-snake-ont_1a_readids_by_adapter_type
description: Use this skill when orchestrating the retained "ont_1a_readIDs_by_adapter_type" step of the mckellardw slide_snake finish finish workflow. It keeps the ont 1a readIDs by adapter type stage tied to upstream `ont_1a_call_adapter_scan` and the downstream handoff to `ont_1a_adapter_scan_summary`. It tracks completion via `results/finish/ont_1a_readIDs_by_adapter_type.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ont_1a_readIDs_by_adapter_type
  step_name: ont 1a readIDs by adapter type
---

# Scope
Use this skill only for the `ont_1a_readIDs_by_adapter_type` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ont_1a_call_adapter_scan`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ont_1a_readIDs_by_adapter_type.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ont_1a_readIDs_by_adapter_type.done`
- Representative outputs: `results/finish/ont_1a_readIDs_by_adapter_type.done`
- Execution targets: `ont_1a_readIDs_by_adapter_type`
- Downstream handoff: `ont_1a_adapter_scan_summary`

## Guardrails
- Treat `results/finish/ont_1a_readIDs_by_adapter_type.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ont_1a_readIDs_by_adapter_type.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ont_1a_adapter_scan_summary` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ont_1a_readIDs_by_adapter_type.done` exists and `ont_1a_adapter_scan_summary` can proceed without re-running ont 1a readIDs by adapter type.
