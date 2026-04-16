---
name: finish-snakemake-workflows-single-cell-rna-seq-hvg_pca
description: Use this skill when orchestrating the retained "hvg_pca" step of the snakemake workflows single cell rna seq finish finish workflow. It keeps the hvg pca stage tied to upstream `correlation` and the downstream handoff to `hvg_tsne`. It tracks completion via `results/finish/hvg_pca.done`.
metadata:
  workflow_id: single-cell-rna-seq-finish
  workflow_name: snakemake workflows single cell rna seq finish
  step_id: hvg_pca
  step_name: hvg pca
---

# Scope
Use this skill only for the `hvg_pca` step in `single-cell-rna-seq-finish`.

## Orchestration
- Upstream requirements: `correlation`
- Step file: `finish/single-cell-rna-seq-finish/steps/hvg_pca.smk`
- Config file: `finish/single-cell-rna-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/hvg_pca.done`
- Representative outputs: `results/finish/hvg_pca.done`
- Execution targets: `hvg_pca`
- Downstream handoff: `hvg_tsne`

## Guardrails
- Treat `results/finish/hvg_pca.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/hvg_pca.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `hvg_tsne` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/hvg_pca.done` exists and `hvg_tsne` can proceed without re-running hvg pca.
