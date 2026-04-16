---
name: finish-mckellardw-slide-snake-bc_copy_barcode_map
description: Use this skill when orchestrating the retained "BC_copy_barcode_map" step of the mckellardw slide_snake finish finish workflow. It keeps the BC copy barcode map stage tied to upstream `utils_index_BAM` and the downstream handoff to `BC_get_simple_whitelist`. It tracks completion via `results/finish/BC_copy_barcode_map.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: BC_copy_barcode_map
  step_name: BC copy barcode map
---

# Scope
Use this skill only for the `BC_copy_barcode_map` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `utils_index_BAM`
- Step file: `finish/mckellardw-slide_snake-finish/steps/BC_copy_barcode_map.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/BC_copy_barcode_map.done`
- Representative outputs: `results/finish/BC_copy_barcode_map.done`
- Execution targets: `BC_copy_barcode_map`
- Downstream handoff: `BC_get_simple_whitelist`

## Guardrails
- Treat `results/finish/BC_copy_barcode_map.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/BC_copy_barcode_map.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `BC_get_simple_whitelist` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/BC_copy_barcode_map.done` exists and `BC_get_simple_whitelist` can proceed without re-running BC copy barcode map.
