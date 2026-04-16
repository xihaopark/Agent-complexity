---
name: finish-snakemake-workflows-single-cell-rna-seq-filter_cells
description: Use this skill when orchestrating the retained "filter_cells" step of the snakemake workflows single cell rna seq finish finish workflow. It keeps the filter cells stage tied to upstream `gene_tsne` and the downstream handoff to `cell_cycle`. It tracks completion via `results/finish/filter_cells.done`.
metadata:
  workflow_id: single-cell-rna-seq-finish
  workflow_name: snakemake workflows single cell rna seq finish
  step_id: filter_cells
  step_name: filter cells
---

# Scope
Use this skill only for the `filter_cells` step in `single-cell-rna-seq-finish`.

## Orchestration
- Upstream requirements: `gene_tsne`
- Step file: `finish/single-cell-rna-seq-finish/steps/filter_cells.smk`
- Config file: `finish/single-cell-rna-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/filter_cells.done`
- Representative outputs: `results/finish/filter_cells.done`
- Execution targets: `filter_cells`
- Downstream handoff: `cell_cycle`

## Guardrails
- Treat `results/finish/filter_cells.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/filter_cells.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `cell_cycle` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/filter_cells.done` exists and `cell_cycle` can proceed without re-running filter cells.
