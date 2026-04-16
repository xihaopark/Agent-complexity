---
name: finish-snakemake-workflows-rna-seq-star-deseq2-gene_2_symbol
description: Use this skill when orchestrating the retained "gene_2_symbol" step of the snakemake workflows rna seq star deseq2 finish finish workflow. It keeps the gene 2 symbol stage tied to upstream `count_matrix` and the downstream handoff to `deseq2_init`. It tracks completion via `results/finish/gene_2_symbol.done`.
metadata:
  workflow_id: rna-seq-star-deseq2-finish
  workflow_name: snakemake workflows rna seq star deseq2 finish
  step_id: gene_2_symbol
  step_name: gene 2 symbol
---

# Scope
Use this skill only for the `gene_2_symbol` step in `rna-seq-star-deseq2-finish`.

## Orchestration
- Upstream requirements: `count_matrix`
- Step file: `finish/rna-seq-star-deseq2-finish/steps/gene_2_symbol.smk`
- Config file: `finish/rna-seq-star-deseq2-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/gene_2_symbol.done`
- Representative outputs: `results/finish/gene_2_symbol.done`
- Execution targets: `gene_2_symbol`
- Downstream handoff: `deseq2_init`

## Guardrails
- Treat `results/finish/gene_2_symbol.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/gene_2_symbol.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `deseq2_init` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/gene_2_symbol.done` exists and `deseq2_init` can proceed without re-running gene 2 symbol.
