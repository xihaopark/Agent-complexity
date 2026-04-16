---
name: finish-star-deseq2-differential-expression
description: Use this skill when orchestrating the retained "differential_expression" step of the RNA-seq STAR DESeq2 finish workflow. It ties the DESeq2 analysis to its count-matrix prerequisite, expected differential-expression outputs, and the downstream PCA plotting handoff.
metadata:
  workflow_id: rna-seq-star-deseq2-finish
  workflow_name: RNA-seq STAR DESeq2 Finish Workflow
  step_id: differential_expression
  step_name: Run DESeq2 differential expression
---

# Scope
Use this skill only for the `differential_expression` step in `rna-seq-star-deseq2-finish`.

## Orchestration
- Upstream requirements: `count_matrix`
- Step file: `finish/rna-seq-star-deseq2-finish/steps/differential_expression.smk`
- Config file: `finish/rna-seq-star-deseq2-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/deseq2/all.rds`, `results/deseq2/normcounts.symbol.tsv`, `results/diffexp/*.tsv`, `results/diffexp/*.svg`
- Representative outputs: `results/deseq2/all.rds`, `results/deseq2/normcounts.symbol.tsv`, `results/diffexp/*.diffexp.symbol.tsv`, `results/diffexp/*.ma-plot.svg`
- Execution targets: `results/deseq2/all.rds`, `results/deseq2/normcounts.symbol.tsv`, `results/diffexp/*.diffexp.symbol.tsv`
- Downstream handoff: `pca_plot`

## Guardrails
- This workflow slice does not emit a finish stamp; validate completion against the DESeq2 object, normalized counts, and contrast-specific diffexp outputs.
- Keep this stage focused on DESeq2 and contrast outputs; PCA visualization remains a downstream presentation step.

## Done Criteria
Mark this step complete only when the DESeq2 model outputs and differential-expression reports exist and the PCA stage can consume them directly.
