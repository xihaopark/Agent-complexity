---
name: finish-mckellardw-slide-snake-ilmn_3a_cache_h5ad_star
description: Use this skill when orchestrating the retained "ilmn_3a_cache_h5ad_STAR" step of the mckellardw slide_snake finish finish workflow. It keeps the ilmn 3a cache h5ad STAR stage tied to upstream `ilmn_3a_cache_seurat_STAR` and the downstream handoff to `ilmn_3b_fastqc_unmapped`. It tracks completion via `results/finish/ilmn_3a_cache_h5ad_STAR.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ilmn_3a_cache_h5ad_STAR
  step_name: ilmn 3a cache h5ad STAR
---

# Scope
Use this skill only for the `ilmn_3a_cache_h5ad_STAR` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ilmn_3a_cache_seurat_STAR`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ilmn_3a_cache_h5ad_STAR.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ilmn_3a_cache_h5ad_STAR.done`
- Representative outputs: `results/finish/ilmn_3a_cache_h5ad_STAR.done`
- Execution targets: `ilmn_3a_cache_h5ad_STAR`
- Downstream handoff: `ilmn_3b_fastqc_unmapped`

## Guardrails
- Treat `results/finish/ilmn_3a_cache_h5ad_STAR.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ilmn_3a_cache_h5ad_STAR.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ilmn_3b_fastqc_unmapped` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ilmn_3a_cache_h5ad_STAR.done` exists and `ilmn_3b_fastqc_unmapped` can proceed without re-running ilmn 3a cache h5ad STAR.
