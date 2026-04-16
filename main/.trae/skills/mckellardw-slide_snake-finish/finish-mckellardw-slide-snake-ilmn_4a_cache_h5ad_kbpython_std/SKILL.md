---
name: finish-mckellardw-slide-snake-ilmn_4a_cache_h5ad_kbpython_std
description: Use this skill when orchestrating the retained "ilmn_4a_cache_h5ad_kbpython_std" step of the mckellardw slide_snake finish finish workflow. It keeps the ilmn 4a cache h5ad kbpython std stage tied to upstream `ilmn_4a_cache_seurat_kbpython_std` and the downstream handoff to `ilmn_5a_copy_R2_fq_for_mirge`. It tracks completion via `results/finish/ilmn_4a_cache_h5ad_kbpython_std.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ilmn_4a_cache_h5ad_kbpython_std
  step_name: ilmn 4a cache h5ad kbpython std
---

# Scope
Use this skill only for the `ilmn_4a_cache_h5ad_kbpython_std` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ilmn_4a_cache_seurat_kbpython_std`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ilmn_4a_cache_h5ad_kbpython_std.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ilmn_4a_cache_h5ad_kbpython_std.done`
- Representative outputs: `results/finish/ilmn_4a_cache_h5ad_kbpython_std.done`
- Execution targets: `ilmn_4a_cache_h5ad_kbpython_std`
- Downstream handoff: `ilmn_5a_copy_R2_fq_for_mirge`

## Guardrails
- Treat `results/finish/ilmn_4a_cache_h5ad_kbpython_std.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ilmn_4a_cache_h5ad_kbpython_std.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ilmn_5a_copy_R2_fq_for_mirge` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ilmn_4a_cache_h5ad_kbpython_std.done` exists and `ilmn_5a_copy_R2_fq_for_mirge` can proceed without re-running ilmn 4a cache h5ad kbpython std.
