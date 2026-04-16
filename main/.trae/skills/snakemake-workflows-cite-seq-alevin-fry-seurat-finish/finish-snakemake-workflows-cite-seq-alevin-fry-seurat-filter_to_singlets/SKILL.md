---
name: finish-snakemake-workflows-cite-seq-alevin-fry-seurat-filter_to_singlets
description: Use this skill when orchestrating the retained "filter_to_singlets" step of the snakemake workflows cite seq alevin fry seurat finish finish workflow. It keeps the filter to singlets stage tied to upstream `plot_umap_singlets_doublets` and the downstream handoff to `all`. It tracks completion via `results/finish/filter_to_singlets.done`.
metadata:
  workflow_id: cite-seq-alevin-fry-seurat-finish
  workflow_name: snakemake workflows cite seq alevin fry seurat finish
  step_id: filter_to_singlets
  step_name: filter to singlets
---

# Scope
Use this skill only for the `filter_to_singlets` step in `cite-seq-alevin-fry-seurat-finish`.

## Orchestration
- Upstream requirements: `plot_umap_singlets_doublets`
- Step file: `finish/cite-seq-alevin-fry-seurat-finish/steps/filter_to_singlets.smk`
- Config file: `finish/cite-seq-alevin-fry-seurat-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/filter_to_singlets.done`
- Representative outputs: `results/finish/filter_to_singlets.done`
- Execution targets: `filter_to_singlets`
- Downstream handoff: `all`

## Guardrails
- Treat `results/finish/filter_to_singlets.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/filter_to_singlets.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `all` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/filter_to_singlets.done` exists and `all` can proceed without re-running filter to singlets.
