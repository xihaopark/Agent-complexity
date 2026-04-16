---
name: finish-mckellardw-slide-snake-ont_2d_ultra_sort_compress_output
description: Use this skill when orchestrating the retained "ont_2d_ultra_sort_compress_output" step of the mckellardw slide_snake finish finish workflow. It keeps the ont 2d ultra sort compress output stage tied to upstream `ont_2d_ultra_pipeline_genome` and the downstream handoff to `ont_2d_ultra_add_corrected_barcodes`. It tracks completion via `results/finish/ont_2d_ultra_sort_compress_output.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ont_2d_ultra_sort_compress_output
  step_name: ont 2d ultra sort compress output
---

# Scope
Use this skill only for the `ont_2d_ultra_sort_compress_output` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ont_2d_ultra_pipeline_genome`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ont_2d_ultra_sort_compress_output.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ont_2d_ultra_sort_compress_output.done`
- Representative outputs: `results/finish/ont_2d_ultra_sort_compress_output.done`
- Execution targets: `ont_2d_ultra_sort_compress_output`
- Downstream handoff: `ont_2d_ultra_add_corrected_barcodes`

## Guardrails
- Treat `results/finish/ont_2d_ultra_sort_compress_output.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ont_2d_ultra_sort_compress_output.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ont_2d_ultra_add_corrected_barcodes` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ont_2d_ultra_sort_compress_output.done` exists and `ont_2d_ultra_add_corrected_barcodes` can proceed without re-running ont 2d ultra sort compress output.
