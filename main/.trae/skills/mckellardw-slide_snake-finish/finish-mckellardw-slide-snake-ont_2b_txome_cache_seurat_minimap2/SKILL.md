---
name: finish-mckellardw-slide-snake-ont_2b_txome_cache_seurat_minimap2
description: Use this skill when orchestrating the retained "ont_2b_txome_cache_seurat_minimap2" step of the mckellardw slide_snake finish finish workflow. It keeps the ont 2b txome cache seurat minimap2 stage tied to upstream `ont_2b_txome_cache_h5ad_minimap2` and the downstream handoff to `ont_1f_sort_gtf`. It tracks completion via `results/finish/ont_2b_txome_cache_seurat_minimap2.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ont_2b_txome_cache_seurat_minimap2
  step_name: ont 2b txome cache seurat minimap2
---

# Scope
Use this skill only for the `ont_2b_txome_cache_seurat_minimap2` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ont_2b_txome_cache_h5ad_minimap2`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ont_2b_txome_cache_seurat_minimap2.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ont_2b_txome_cache_seurat_minimap2.done`
- Representative outputs: `results/finish/ont_2b_txome_cache_seurat_minimap2.done`
- Execution targets: `ont_2b_txome_cache_seurat_minimap2`
- Downstream handoff: `ont_1f_sort_gtf`

## Guardrails
- Treat `results/finish/ont_2b_txome_cache_seurat_minimap2.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ont_2b_txome_cache_seurat_minimap2.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ont_1f_sort_gtf` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ont_2b_txome_cache_seurat_minimap2.done` exists and `ont_1f_sort_gtf` can proceed without re-running ont 2b txome cache seurat minimap2.
