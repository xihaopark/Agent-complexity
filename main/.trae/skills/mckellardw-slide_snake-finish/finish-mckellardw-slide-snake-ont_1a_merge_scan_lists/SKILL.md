---
name: finish-mckellardw-slide-snake-ont_1a_merge_scan_lists
description: Use this skill when orchestrating the retained "ont_1a_merge_scan_lists" step of the mckellardw slide_snake finish finish workflow. It keeps the ont 1a merge scan lists stage tied to upstream `ont_1a_adapter_scan_summary` and the downstream handoff to `ont_1a_subset_fastq_by_adapter_type`. It tracks completion via `results/finish/ont_1a_merge_scan_lists.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ont_1a_merge_scan_lists
  step_name: ont 1a merge scan lists
---

# Scope
Use this skill only for the `ont_1a_merge_scan_lists` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ont_1a_adapter_scan_summary`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ont_1a_merge_scan_lists.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ont_1a_merge_scan_lists.done`
- Representative outputs: `results/finish/ont_1a_merge_scan_lists.done`
- Execution targets: `ont_1a_merge_scan_lists`
- Downstream handoff: `ont_1a_subset_fastq_by_adapter_type`

## Guardrails
- Treat `results/finish/ont_1a_merge_scan_lists.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ont_1a_merge_scan_lists.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ont_1a_subset_fastq_by_adapter_type` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ont_1a_merge_scan_lists.done` exists and `ont_1a_subset_fastq_by_adapter_type` can proceed without re-running ont 1a merge scan lists.
