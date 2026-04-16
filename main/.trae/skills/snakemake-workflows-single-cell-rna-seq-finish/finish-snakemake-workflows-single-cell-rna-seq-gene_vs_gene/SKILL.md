---
name: finish-snakemake-workflows-single-cell-rna-seq-gene_vs_gene
description: Use this skill when orchestrating the retained "gene_vs_gene" step of the snakemake workflows single cell rna seq finish finish workflow. It keeps the gene vs gene stage tied to upstream `explained_variance` and the downstream handoff to `gene_tsne`. It tracks completion via `results/finish/gene_vs_gene.done`.
metadata:
  workflow_id: single-cell-rna-seq-finish
  workflow_name: snakemake workflows single cell rna seq finish
  step_id: gene_vs_gene
  step_name: gene vs gene
---

# Scope
Use this skill only for the `gene_vs_gene` step in `single-cell-rna-seq-finish`.

## Orchestration
- Upstream requirements: `explained_variance`
- Step file: `finish/single-cell-rna-seq-finish/steps/gene_vs_gene.smk`
- Config file: `finish/single-cell-rna-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/gene_vs_gene.done`
- Representative outputs: `results/finish/gene_vs_gene.done`
- Execution targets: `gene_vs_gene`
- Downstream handoff: `gene_tsne`

## Guardrails
- Treat `results/finish/gene_vs_gene.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/gene_vs_gene.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `gene_tsne` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/gene_vs_gene.done` exists and `gene_tsne` can proceed without re-running gene vs gene.
