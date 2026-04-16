---
name: finish-snakemake-workflows-single-cell-rna-seq-gene_tsne
description: Use this skill when orchestrating the retained "gene_tsne" step of the snakemake workflows single cell rna seq finish finish workflow. It keeps the gene tsne stage tied to upstream `gene_vs_gene` and the downstream handoff to `filter_cells`. It tracks completion via `results/finish/gene_tsne.done`.
metadata:
  workflow_id: single-cell-rna-seq-finish
  workflow_name: snakemake workflows single cell rna seq finish
  step_id: gene_tsne
  step_name: gene tsne
---

# Scope
Use this skill only for the `gene_tsne` step in `single-cell-rna-seq-finish`.

## Orchestration
- Upstream requirements: `gene_vs_gene`
- Step file: `finish/single-cell-rna-seq-finish/steps/gene_tsne.smk`
- Config file: `finish/single-cell-rna-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/gene_tsne.done`
- Representative outputs: `results/finish/gene_tsne.done`
- Execution targets: `gene_tsne`
- Downstream handoff: `filter_cells`

## Guardrails
- Treat `results/finish/gene_tsne.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/gene_tsne.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `filter_cells` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/gene_tsne.done` exists and `filter_cells` can proceed without re-running gene tsne.
