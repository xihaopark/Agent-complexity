---
name: finish-mckellardw-slide-snake-ont_2d_ultra_counts_to_sparse
description: Use this skill when orchestrating the retained "ont_2d_ultra_counts_to_sparse" step of the mckellardw slide_snake finish finish workflow. It keeps the ont 2d ultra counts to sparse stage tied to upstream `ont_2d_ultra_umitools_count` and the downstream handoff to `ont_2d_ultra_cache_h5ad`. It tracks completion via `results/finish/ont_2d_ultra_counts_to_sparse.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ont_2d_ultra_counts_to_sparse
  step_name: ont 2d ultra counts to sparse
---

# Scope
Use this skill only for the `ont_2d_ultra_counts_to_sparse` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ont_2d_ultra_umitools_count`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ont_2d_ultra_counts_to_sparse.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ont_2d_ultra_counts_to_sparse.done`
- Representative outputs: `results/finish/ont_2d_ultra_counts_to_sparse.done`
- Execution targets: `ont_2d_ultra_counts_to_sparse`
- Downstream handoff: `ont_2d_ultra_cache_h5ad`

## Guardrails
- Treat `results/finish/ont_2d_ultra_counts_to_sparse.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ont_2d_ultra_counts_to_sparse.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ont_2d_ultra_cache_h5ad` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ont_2d_ultra_counts_to_sparse.done` exists and `ont_2d_ultra_cache_h5ad` can proceed without re-running ont 2d ultra counts to sparse.
