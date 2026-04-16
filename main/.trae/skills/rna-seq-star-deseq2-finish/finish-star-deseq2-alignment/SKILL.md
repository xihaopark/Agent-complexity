---
name: finish-star-deseq2-alignment
description: Use this skill when orchestrating the retained "alignment" step of the RNA-seq STAR DESeq2 finish workflow. It keeps the STAR alignment stage tied to its trimming dependency, expected BAM and gene count outputs, and the downstream QC and count-matrix fan-out.
metadata:
  workflow_id: rna-seq-star-deseq2-finish
  workflow_name: RNA-seq STAR DESeq2 Finish Workflow
  step_id: alignment
  step_name: Align reads with STAR
---

# Scope
Use this skill only for the `alignment` step in `rna-seq-star-deseq2-finish`.

## Orchestration
- Upstream requirements: `trimming`
- Step file: `finish/rna-seq-star-deseq2-finish/steps/alignment.smk`
- Config file: `finish/rna-seq-star-deseq2-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/star/*/Aligned.sortedByCoord.out.bam`, `results/star/*/ReadsPerGene.out.tab`
- Representative outputs: `results/star/*/Aligned.sortedByCoord.out.bam`, `results/star/*/ReadsPerGene.out.tab`, `resources/star_genome`
- Execution targets: `results/star/*/Aligned.sortedByCoord.out.bam`, `results/star/*/ReadsPerGene.out.tab`
- Downstream handoff: `rseqc_qc`, `count_matrix`

## Guardrails
- This workflow slice does not emit a finish stamp; validate completion against the STAR BAM and gene-count outputs.
- Preserve the dual handoff contract: alignment must unlock both QC and count-matrix branches from the same alignment state.

## Done Criteria
Mark this step complete only when every planned sample has aligned BAM and gene count tab outputs and both downstream branches can consume them directly.
