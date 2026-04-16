---
name: finish-star-deseq2-count-matrix
description: Use this skill when orchestrating the retained "count_matrix" step of the RNA-seq STAR DESeq2 finish workflow. It covers the alignment dependency, count-matrix outputs, and the handoff into differential expression analysis.
metadata:
  workflow_id: rna-seq-star-deseq2-finish
  workflow_name: RNA-seq STAR DESeq2 Finish Workflow
  step_id: count_matrix
  step_name: Build count matrix
---

# Scope
Use this skill only for the `count_matrix` step in `rna-seq-star-deseq2-finish`.

## Orchestration
- Upstream requirements: `alignment`
- Step file: `finish/rna-seq-star-deseq2-finish/steps/count_matrix.smk`
- Config file: `finish/rna-seq-star-deseq2-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/counts/all.tsv`, `results/counts/all.symbol.tsv`
- Representative outputs: `results/counts/all.tsv`, `results/counts/all.symbol.tsv`
- Execution targets: `results/counts/all.tsv`, `results/counts/all.symbol.tsv`
- Downstream handoff: `differential_expression`

## Guardrails
- This workflow slice does not emit a finish stamp; validate completion against the merged count tables themselves.
- Keep this stage focused on count-matrix assembly and symbol annotation, not on downstream DESeq2 fitting.

## Done Criteria
Mark this step complete only when the merged count tables are present and ready for DESeq2 without additional alignment processing.
