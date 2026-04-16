---
name: finish-mckellardw-slide-snake-ont_1f_sort_gtf
description: Use this skill when orchestrating the retained "ont_1f_sort_gtf" step of the mckellardw slide_snake finish finish workflow. It keeps the ont 1f sort gtf stage tied to upstream `ont_2b_txome_cache_seurat_minimap2` and the downstream handoff to `ont_2d_ultra_pipeline_genome`. It tracks completion via `results/finish/ont_1f_sort_gtf.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ont_1f_sort_gtf
  step_name: ont 1f sort gtf
---

# Scope
Use this skill only for the `ont_1f_sort_gtf` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ont_2b_txome_cache_seurat_minimap2`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ont_1f_sort_gtf.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ont_1f_sort_gtf.done`
- Representative outputs: `results/finish/ont_1f_sort_gtf.done`
- Execution targets: `ont_1f_sort_gtf`
- Downstream handoff: `ont_2d_ultra_pipeline_genome`

## Guardrails
- Treat `results/finish/ont_1f_sort_gtf.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ont_1f_sort_gtf.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ont_2d_ultra_pipeline_genome` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ont_1f_sort_gtf.done` exists and `ont_2d_ultra_pipeline_genome` can proceed without re-running ont 1f sort gtf.
