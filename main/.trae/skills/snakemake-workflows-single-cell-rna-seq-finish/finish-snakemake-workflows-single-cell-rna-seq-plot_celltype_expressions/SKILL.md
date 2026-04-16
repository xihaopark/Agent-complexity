---
name: finish-snakemake-workflows-single-cell-rna-seq-plot_celltype_expressions
description: Use this skill when orchestrating the retained "plot_celltype_expressions" step of the snakemake workflows single cell rna seq finish finish workflow. It keeps the plot celltype expressions stage tied to upstream `celltype_tsne` and the downstream handoff to `edger`. It tracks completion via `results/finish/plot_celltype_expressions.done`.
metadata:
  workflow_id: single-cell-rna-seq-finish
  workflow_name: snakemake workflows single cell rna seq finish
  step_id: plot_celltype_expressions
  step_name: plot celltype expressions
---

# Scope
Use this skill only for the `plot_celltype_expressions` step in `single-cell-rna-seq-finish`.

## Orchestration
- Upstream requirements: `celltype_tsne`
- Step file: `finish/single-cell-rna-seq-finish/steps/plot_celltype_expressions.smk`
- Config file: `finish/single-cell-rna-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plot_celltype_expressions.done`
- Representative outputs: `results/finish/plot_celltype_expressions.done`
- Execution targets: `plot_celltype_expressions`
- Downstream handoff: `edger`

## Guardrails
- Treat `results/finish/plot_celltype_expressions.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plot_celltype_expressions.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `edger` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plot_celltype_expressions.done` exists and `edger` can proceed without re-running plot celltype expressions.
