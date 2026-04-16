---
name: finish-snakemake-workflows-single-cell-rna-seq-hvg_tsne
description: Use this skill when orchestrating the retained "hvg_tsne" step of the snakemake workflows single cell rna seq finish finish workflow. It keeps the hvg tsne stage tied to upstream `hvg_pca` and the downstream handoff to `cellassign`. It tracks completion via `results/finish/hvg_tsne.done`.
metadata:
  workflow_id: single-cell-rna-seq-finish
  workflow_name: snakemake workflows single cell rna seq finish
  step_id: hvg_tsne
  step_name: hvg tsne
---

# Scope
Use this skill only for the `hvg_tsne` step in `single-cell-rna-seq-finish`.

## Orchestration
- Upstream requirements: `hvg_pca`
- Step file: `finish/single-cell-rna-seq-finish/steps/hvg_tsne.smk`
- Config file: `finish/single-cell-rna-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/hvg_tsne.done`
- Representative outputs: `results/finish/hvg_tsne.done`
- Execution targets: `hvg_tsne`
- Downstream handoff: `cellassign`

## Guardrails
- Treat `results/finish/hvg_tsne.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/hvg_tsne.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `cellassign` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/hvg_tsne.done` exists and `cellassign` can proceed without re-running hvg tsne.
