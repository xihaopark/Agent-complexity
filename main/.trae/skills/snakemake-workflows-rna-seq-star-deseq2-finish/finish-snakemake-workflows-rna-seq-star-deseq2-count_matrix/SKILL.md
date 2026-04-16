---
name: finish-snakemake-workflows-rna-seq-star-deseq2-count_matrix
description: Use this skill when orchestrating the retained "count_matrix" step of the snakemake workflows rna seq star deseq2 finish finish workflow. It keeps the count matrix stage tied to upstream `star_align` and the downstream handoff to `gene_2_symbol`. It tracks completion via `results/finish/count_matrix.done`.
metadata:
  workflow_id: rna-seq-star-deseq2-finish
  workflow_name: snakemake workflows rna seq star deseq2 finish
  step_id: count_matrix
  step_name: count matrix
---

# Scope
Use this skill only for the `count_matrix` step in `rna-seq-star-deseq2-finish`.

## Orchestration
- Upstream requirements: `star_align`
- Step file: `finish/rna-seq-star-deseq2-finish/steps/count_matrix.smk`
- Config file: `finish/rna-seq-star-deseq2-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/count_matrix.done`
- Representative outputs: `results/finish/count_matrix.done`
- Execution targets: `count_matrix`
- Downstream handoff: `gene_2_symbol`

## Guardrails
- Treat `results/finish/count_matrix.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/count_matrix.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `gene_2_symbol` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/count_matrix.done` exists and `gene_2_symbol` can proceed without re-running count matrix.
