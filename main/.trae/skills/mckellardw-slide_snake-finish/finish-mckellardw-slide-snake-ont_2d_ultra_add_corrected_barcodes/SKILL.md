---
name: finish-mckellardw-slide-snake-ont_2d_ultra_add_corrected_barcodes
description: Use this skill when orchestrating the retained "ont_2d_ultra_add_corrected_barcodes" step of the mckellardw slide_snake finish finish workflow. It keeps the ont 2d ultra add corrected barcodes stage tied to upstream `ont_2d_ultra_sort_compress_output` and the downstream handoff to `ont_2d_ultra_add_umis`. It tracks completion via `results/finish/ont_2d_ultra_add_corrected_barcodes.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ont_2d_ultra_add_corrected_barcodes
  step_name: ont 2d ultra add corrected barcodes
---

# Scope
Use this skill only for the `ont_2d_ultra_add_corrected_barcodes` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ont_2d_ultra_sort_compress_output`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ont_2d_ultra_add_corrected_barcodes.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ont_2d_ultra_add_corrected_barcodes.done`
- Representative outputs: `results/finish/ont_2d_ultra_add_corrected_barcodes.done`
- Execution targets: `ont_2d_ultra_add_corrected_barcodes`
- Downstream handoff: `ont_2d_ultra_add_umis`

## Guardrails
- Treat `results/finish/ont_2d_ultra_add_corrected_barcodes.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ont_2d_ultra_add_corrected_barcodes.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ont_2d_ultra_add_umis` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ont_2d_ultra_add_corrected_barcodes.done` exists and `ont_2d_ultra_add_umis` can proceed without re-running ont 2d ultra add corrected barcodes.
