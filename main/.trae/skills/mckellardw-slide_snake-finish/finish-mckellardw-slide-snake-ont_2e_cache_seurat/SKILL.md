---
name: finish-mckellardw-slide-snake-ont_2e_cache_seurat
description: Use this skill when orchestrating the retained "ont_2e_cache_seurat" step of the mckellardw slide_snake finish finish workflow. It keeps the ont 2e cache seurat stage tied to upstream `ont_2e_cache_h5ad` and the downstream handoff to `ont_3a_readQC_0_rawInput`. It tracks completion via `results/finish/ont_2e_cache_seurat.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ont_2e_cache_seurat
  step_name: ont 2e cache seurat
---

# Scope
Use this skill only for the `ont_2e_cache_seurat` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ont_2e_cache_h5ad`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ont_2e_cache_seurat.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ont_2e_cache_seurat.done`
- Representative outputs: `results/finish/ont_2e_cache_seurat.done`
- Execution targets: `ont_2e_cache_seurat`
- Downstream handoff: `ont_3a_readQC_0_rawInput`

## Guardrails
- Treat `results/finish/ont_2e_cache_seurat.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ont_2e_cache_seurat.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ont_3a_readQC_0_rawInput` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ont_2e_cache_seurat.done` exists and `ont_3a_readQC_0_rawInput` can proceed without re-running ont 2e cache seurat.
