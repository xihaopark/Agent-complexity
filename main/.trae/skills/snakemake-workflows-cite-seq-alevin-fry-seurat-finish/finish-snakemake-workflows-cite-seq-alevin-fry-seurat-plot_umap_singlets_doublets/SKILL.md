---
name: finish-snakemake-workflows-cite-seq-alevin-fry-seurat-plot_umap_singlets_doublets
description: Use this skill when orchestrating the retained "plot_umap_singlets_doublets" step of the snakemake workflows cite seq alevin fry seurat finish finish workflow. It keeps the plot umap singlets doublets stage tied to upstream `filter_negatives` and the downstream handoff to `filter_to_singlets`. It tracks completion via `results/finish/plot_umap_singlets_doublets.done`.
metadata:
  workflow_id: cite-seq-alevin-fry-seurat-finish
  workflow_name: snakemake workflows cite seq alevin fry seurat finish
  step_id: plot_umap_singlets_doublets
  step_name: plot umap singlets doublets
---

# Scope
Use this skill only for the `plot_umap_singlets_doublets` step in `cite-seq-alevin-fry-seurat-finish`.

## Orchestration
- Upstream requirements: `filter_negatives`
- Step file: `finish/cite-seq-alevin-fry-seurat-finish/steps/plot_umap_singlets_doublets.smk`
- Config file: `finish/cite-seq-alevin-fry-seurat-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plot_umap_singlets_doublets.done`
- Representative outputs: `results/finish/plot_umap_singlets_doublets.done`
- Execution targets: `plot_umap_singlets_doublets`
- Downstream handoff: `filter_to_singlets`

## Guardrails
- Treat `results/finish/plot_umap_singlets_doublets.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plot_umap_singlets_doublets.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `filter_to_singlets` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plot_umap_singlets_doublets.done` exists and `filter_to_singlets` can proceed without re-running plot umap singlets doublets.
