---
name: finish-mckellardw-slide-snake-bc_get_simple_whitelist
description: Use this skill when orchestrating the retained "BC_get_simple_whitelist" step of the mckellardw slide_snake finish finish workflow. It keeps the BC get simple whitelist stage tied to upstream `BC_copy_barcode_map` and the downstream handoff to `BC_write_whitelist_variants`. It tracks completion via `results/finish/BC_get_simple_whitelist.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: BC_get_simple_whitelist
  step_name: BC get simple whitelist
---

# Scope
Use this skill only for the `BC_get_simple_whitelist` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `BC_copy_barcode_map`
- Step file: `finish/mckellardw-slide_snake-finish/steps/BC_get_simple_whitelist.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/BC_get_simple_whitelist.done`
- Representative outputs: `results/finish/BC_get_simple_whitelist.done`
- Execution targets: `BC_get_simple_whitelist`
- Downstream handoff: `BC_write_whitelist_variants`

## Guardrails
- Treat `results/finish/BC_get_simple_whitelist.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/BC_get_simple_whitelist.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `BC_write_whitelist_variants` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/BC_get_simple_whitelist.done` exists and `BC_write_whitelist_variants` can proceed without re-running BC get simple whitelist.
