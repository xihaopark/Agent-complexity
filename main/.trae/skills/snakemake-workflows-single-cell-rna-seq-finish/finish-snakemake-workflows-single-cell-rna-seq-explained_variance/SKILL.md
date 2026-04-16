---
name: finish-snakemake-workflows-single-cell-rna-seq-explained_variance
description: Use this skill when orchestrating the retained "explained_variance" step of the snakemake workflows single cell rna seq finish finish workflow. It keeps the explained variance stage tied to upstream `qc` and the downstream handoff to `gene_vs_gene`. It tracks completion via `results/finish/explained_variance.done`.
metadata:
  workflow_id: single-cell-rna-seq-finish
  workflow_name: snakemake workflows single cell rna seq finish
  step_id: explained_variance
  step_name: explained variance
---

# Scope
Use this skill only for the `explained_variance` step in `single-cell-rna-seq-finish`.

## Orchestration
- Upstream requirements: `qc`
- Step file: `finish/single-cell-rna-seq-finish/steps/explained_variance.smk`
- Config file: `finish/single-cell-rna-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/explained_variance.done`
- Representative outputs: `results/finish/explained_variance.done`
- Execution targets: `explained_variance`
- Downstream handoff: `gene_vs_gene`

## Guardrails
- Treat `results/finish/explained_variance.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/explained_variance.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `gene_vs_gene` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/explained_variance.done` exists and `gene_vs_gene` can proceed without re-running explained variance.
