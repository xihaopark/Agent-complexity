---
name: finish-mckellardw-slide-snake-utils_index_bam
description: Use this skill when orchestrating the retained "utils_index_BAM" step of the mckellardw slide_snake finish finish workflow. It keeps the utils index BAM stage and the downstream handoff to `BC_copy_barcode_map`. It tracks completion via `results/finish/utils_index_BAM.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: utils_index_BAM
  step_name: utils index BAM
---

# Scope
Use this skill only for the `utils_index_BAM` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: none
- Step file: `finish/mckellardw-slide_snake-finish/steps/utils_index_BAM.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/utils_index_BAM.done`
- Representative outputs: `results/finish/utils_index_BAM.done`
- Execution targets: `utils_index_BAM`
- Downstream handoff: `BC_copy_barcode_map`

## Guardrails
- Treat `results/finish/utils_index_BAM.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/utils_index_BAM.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `BC_copy_barcode_map` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/utils_index_BAM.done` exists and `BC_copy_barcode_map` can proceed without re-running utils index BAM.
