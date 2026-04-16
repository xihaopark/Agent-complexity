---
name: finish-snakemake-workflows-single-cell-rna-seq-celltype_tsne
description: Use this skill when orchestrating the retained "celltype_tsne" step of the snakemake workflows single cell rna seq finish finish workflow. It keeps the celltype tsne stage tied to upstream `plot_cellassign` and the downstream handoff to `plot_celltype_expressions`. It tracks completion via `results/finish/celltype_tsne.done`.
metadata:
  workflow_id: single-cell-rna-seq-finish
  workflow_name: snakemake workflows single cell rna seq finish
  step_id: celltype_tsne
  step_name: celltype tsne
---

# Scope
Use this skill only for the `celltype_tsne` step in `single-cell-rna-seq-finish`.

## Orchestration
- Upstream requirements: `plot_cellassign`
- Step file: `finish/single-cell-rna-seq-finish/steps/celltype_tsne.smk`
- Config file: `finish/single-cell-rna-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/celltype_tsne.done`
- Representative outputs: `results/finish/celltype_tsne.done`
- Execution targets: `celltype_tsne`
- Downstream handoff: `plot_celltype_expressions`

## Guardrails
- Treat `results/finish/celltype_tsne.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/celltype_tsne.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plot_celltype_expressions` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/celltype_tsne.done` exists and `plot_celltype_expressions` can proceed without re-running celltype tsne.
