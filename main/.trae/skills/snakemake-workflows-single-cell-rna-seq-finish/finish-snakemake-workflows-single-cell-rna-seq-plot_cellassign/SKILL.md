---
name: finish-snakemake-workflows-single-cell-rna-seq-plot_cellassign
description: Use this skill when orchestrating the retained "plot_cellassign" step of the snakemake workflows single cell rna seq finish finish workflow. It keeps the plot cellassign stage tied to upstream `cellassign` and the downstream handoff to `celltype_tsne`. It tracks completion via `results/finish/plot_cellassign.done`.
metadata:
  workflow_id: single-cell-rna-seq-finish
  workflow_name: snakemake workflows single cell rna seq finish
  step_id: plot_cellassign
  step_name: plot cellassign
---

# Scope
Use this skill only for the `plot_cellassign` step in `single-cell-rna-seq-finish`.

## Orchestration
- Upstream requirements: `cellassign`
- Step file: `finish/single-cell-rna-seq-finish/steps/plot_cellassign.smk`
- Config file: `finish/single-cell-rna-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plot_cellassign.done`
- Representative outputs: `results/finish/plot_cellassign.done`
- Execution targets: `plot_cellassign`
- Downstream handoff: `celltype_tsne`

## Guardrails
- Treat `results/finish/plot_cellassign.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plot_cellassign.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `celltype_tsne` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plot_cellassign.done` exists and `celltype_tsne` can proceed without re-running plot cellassign.
