---
name: finish-star-deseq2-pca-plot
description: Use this skill when orchestrating the retained "pca_plot" step of the RNA-seq STAR DESeq2 finish workflow. It captures the final PCA visualization stage, its differential-expression dependency, and the expected terminal artifact for the workflow branch.
metadata:
  workflow_id: rna-seq-star-deseq2-finish
  workflow_name: RNA-seq STAR DESeq2 Finish Workflow
  step_id: pca_plot
  step_name: Generate PCA plot
---

# Scope
Use this skill only for the `pca_plot` step in `rna-seq-star-deseq2-finish`.

## Orchestration
- Upstream requirements: `differential_expression`
- Step file: `finish/rna-seq-star-deseq2-finish/steps/pca_plot.smk`
- Config file: `finish/rna-seq-star-deseq2-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/pca.condition.svg`
- Representative outputs: `results/pca.condition.svg`
- Execution targets: `results/pca.condition.svg`
- Downstream handoff: none

## Guardrails
- This workflow slice does not emit a finish stamp; treat the rendered PCA SVG as the durable completion artifact.
- Keep this terminal step presentation-focused and avoid recomputing differential-expression outputs here.

## Done Criteria
Mark this step complete only when the PCA plot reflects the latest differential-expression outputs and the workflow can be reported as complete for this analysis branch.
