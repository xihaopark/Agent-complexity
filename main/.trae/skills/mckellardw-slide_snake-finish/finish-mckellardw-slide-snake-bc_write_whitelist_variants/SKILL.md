---
name: finish-mckellardw-slide-snake-bc_write_whitelist_variants
description: Use this skill when orchestrating the retained "BC_write_whitelist_variants" step of the mckellardw slide_snake finish finish workflow. It keeps the BC write whitelist variants stage tied to upstream `BC_get_simple_whitelist` and the downstream handoff to `ilmn_1a_merge_fastqs`. It tracks completion via `results/finish/BC_write_whitelist_variants.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: BC_write_whitelist_variants
  step_name: BC write whitelist variants
---

# Scope
Use this skill only for the `BC_write_whitelist_variants` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `BC_get_simple_whitelist`
- Step file: `finish/mckellardw-slide_snake-finish/steps/BC_write_whitelist_variants.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/BC_write_whitelist_variants.done`
- Representative outputs: `results/finish/BC_write_whitelist_variants.done`
- Execution targets: `BC_write_whitelist_variants`
- Downstream handoff: `ilmn_1a_merge_fastqs`

## Guardrails
- Treat `results/finish/BC_write_whitelist_variants.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/BC_write_whitelist_variants.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ilmn_1a_merge_fastqs` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/BC_write_whitelist_variants.done` exists and `ilmn_1a_merge_fastqs` can proceed without re-running BC write whitelist variants.
