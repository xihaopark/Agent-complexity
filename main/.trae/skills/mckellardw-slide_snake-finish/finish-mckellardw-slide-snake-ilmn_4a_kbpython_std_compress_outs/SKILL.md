---
name: finish-mckellardw-slide-snake-ilmn_4a_kbpython_std_compress_outs
description: Use this skill when orchestrating the retained "ilmn_4a_kbpython_std_compress_outs" step of the mckellardw slide_snake finish finish workflow. It keeps the ilmn 4a kbpython std compress outs stage tied to upstream `ilmn_4a_kbpython_std_remove_suffix` and the downstream handoff to `ilmn_4a_cache_seurat_kbpython_std`. It tracks completion via `results/finish/ilmn_4a_kbpython_std_compress_outs.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ilmn_4a_kbpython_std_compress_outs
  step_name: ilmn 4a kbpython std compress outs
---

# Scope
Use this skill only for the `ilmn_4a_kbpython_std_compress_outs` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ilmn_4a_kbpython_std_remove_suffix`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ilmn_4a_kbpython_std_compress_outs.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ilmn_4a_kbpython_std_compress_outs.done`
- Representative outputs: `results/finish/ilmn_4a_kbpython_std_compress_outs.done`
- Execution targets: `ilmn_4a_kbpython_std_compress_outs`
- Downstream handoff: `ilmn_4a_cache_seurat_kbpython_std`

## Guardrails
- Treat `results/finish/ilmn_4a_kbpython_std_compress_outs.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ilmn_4a_kbpython_std_compress_outs.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ilmn_4a_cache_seurat_kbpython_std` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ilmn_4a_kbpython_std_compress_outs.done` exists and `ilmn_4a_cache_seurat_kbpython_std` can proceed without re-running ilmn 4a kbpython std compress outs.
