---
name: finish-snakemake-workflows-single-cell-rna-seq-correlation
description: Use this skill when orchestrating the retained "correlation" step of the snakemake workflows single cell rna seq finish finish workflow. It keeps the correlation stage tied to upstream `hvg` and the downstream handoff to `hvg_pca`. It tracks completion via `results/finish/correlation.done`.
metadata:
  workflow_id: single-cell-rna-seq-finish
  workflow_name: snakemake workflows single cell rna seq finish
  step_id: correlation
  step_name: correlation
---

# Scope
Use this skill only for the `correlation` step in `single-cell-rna-seq-finish`.

## Orchestration
- Upstream requirements: `hvg`
- Step file: `finish/single-cell-rna-seq-finish/steps/correlation.smk`
- Config file: `finish/single-cell-rna-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/correlation.done`
- Representative outputs: `results/finish/correlation.done`
- Execution targets: `correlation`
- Downstream handoff: `hvg_pca`

## Guardrails
- Treat `results/finish/correlation.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/correlation.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `hvg_pca` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/correlation.done` exists and `hvg_pca` can proceed without re-running correlation.
