---
name: finish-snakemake-workflows-single-cell-rna-seq-cellassign
description: Use this skill when orchestrating the retained "cellassign" step of the snakemake workflows single cell rna seq finish finish workflow. It keeps the cellassign stage tied to upstream `hvg_tsne` and the downstream handoff to `plot_cellassign`. It tracks completion via `results/finish/cellassign.done`.
metadata:
  workflow_id: single-cell-rna-seq-finish
  workflow_name: snakemake workflows single cell rna seq finish
  step_id: cellassign
  step_name: cellassign
---

# Scope
Use this skill only for the `cellassign` step in `single-cell-rna-seq-finish`.

## Orchestration
- Upstream requirements: `hvg_tsne`
- Step file: `finish/single-cell-rna-seq-finish/steps/cellassign.smk`
- Config file: `finish/single-cell-rna-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/cellassign.done`
- Representative outputs: `results/finish/cellassign.done`
- Execution targets: `cellassign`
- Downstream handoff: `plot_cellassign`

## Guardrails
- Treat `results/finish/cellassign.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/cellassign.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plot_cellassign` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/cellassign.done` exists and `plot_cellassign` can proceed without re-running cellassign.
