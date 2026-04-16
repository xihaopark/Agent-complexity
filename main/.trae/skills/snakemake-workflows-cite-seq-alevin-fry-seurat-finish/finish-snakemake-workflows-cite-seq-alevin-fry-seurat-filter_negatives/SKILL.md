---
name: finish-snakemake-workflows-cite-seq-alevin-fry-seurat-filter_negatives
description: Use this skill when orchestrating the retained "filter_negatives" step of the snakemake workflows cite seq alevin fry seurat finish finish workflow. It keeps the filter negatives stage tied to upstream `plot_counts_hto_filtered` and the downstream handoff to `plot_umap_singlets_doublets`. It tracks completion via `results/finish/filter_negatives.done`.
metadata:
  workflow_id: cite-seq-alevin-fry-seurat-finish
  workflow_name: snakemake workflows cite seq alevin fry seurat finish
  step_id: filter_negatives
  step_name: filter negatives
---

# Scope
Use this skill only for the `filter_negatives` step in `cite-seq-alevin-fry-seurat-finish`.

## Orchestration
- Upstream requirements: `plot_counts_hto_filtered`
- Step file: `finish/cite-seq-alevin-fry-seurat-finish/steps/filter_negatives.smk`
- Config file: `finish/cite-seq-alevin-fry-seurat-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/filter_negatives.done`
- Representative outputs: `results/finish/filter_negatives.done`
- Execution targets: `filter_negatives`
- Downstream handoff: `plot_umap_singlets_doublets`

## Guardrails
- Treat `results/finish/filter_negatives.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/filter_negatives.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plot_umap_singlets_doublets` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/filter_negatives.done` exists and `plot_umap_singlets_doublets` can proceed without re-running filter negatives.
