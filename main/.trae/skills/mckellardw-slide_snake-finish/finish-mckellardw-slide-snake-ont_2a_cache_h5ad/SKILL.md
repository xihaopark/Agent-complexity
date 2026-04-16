---
name: finish-mckellardw-slide-snake-ont_2a_cache_h5ad
description: Use this skill when orchestrating the retained "ont_2a_cache_h5ad" step of the mckellardw slide_snake finish finish workflow. It keeps the ont 2a cache h5ad stage tied to upstream `ont_2a_counts_to_sparse` and the downstream handoff to `ont_2a_cache_seurat`. It tracks completion via `results/finish/ont_2a_cache_h5ad.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ont_2a_cache_h5ad
  step_name: ont 2a cache h5ad
---

# Scope
Use this skill only for the `ont_2a_cache_h5ad` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ont_2a_counts_to_sparse`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ont_2a_cache_h5ad.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ont_2a_cache_h5ad.done`
- Representative outputs: `results/finish/ont_2a_cache_h5ad.done`
- Execution targets: `ont_2a_cache_h5ad`
- Downstream handoff: `ont_2a_cache_seurat`

## Guardrails
- Treat `results/finish/ont_2a_cache_h5ad.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ont_2a_cache_h5ad.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ont_2a_cache_seurat` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ont_2a_cache_h5ad.done` exists and `ont_2a_cache_seurat` can proceed without re-running ont 2a cache h5ad.
