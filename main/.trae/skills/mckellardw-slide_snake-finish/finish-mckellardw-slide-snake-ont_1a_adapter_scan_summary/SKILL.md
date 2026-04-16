---
name: finish-mckellardw-slide-snake-ont_1a_adapter_scan_summary
description: Use this skill when orchestrating the retained "ont_1a_adapter_scan_summary" step of the mckellardw slide_snake finish finish workflow. It keeps the ont 1a adapter scan summary stage tied to upstream `ont_1a_readIDs_by_adapter_type` and the downstream handoff to `ont_1a_merge_scan_lists`. It tracks completion via `results/finish/ont_1a_adapter_scan_summary.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ont_1a_adapter_scan_summary
  step_name: ont 1a adapter scan summary
---

# Scope
Use this skill only for the `ont_1a_adapter_scan_summary` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ont_1a_readIDs_by_adapter_type`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ont_1a_adapter_scan_summary.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ont_1a_adapter_scan_summary.done`
- Representative outputs: `results/finish/ont_1a_adapter_scan_summary.done`
- Execution targets: `ont_1a_adapter_scan_summary`
- Downstream handoff: `ont_1a_merge_scan_lists`

## Guardrails
- Treat `results/finish/ont_1a_adapter_scan_summary.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ont_1a_adapter_scan_summary.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ont_1a_merge_scan_lists` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ont_1a_adapter_scan_summary.done` exists and `ont_1a_merge_scan_lists` can proceed without re-running ont 1a adapter scan summary.
