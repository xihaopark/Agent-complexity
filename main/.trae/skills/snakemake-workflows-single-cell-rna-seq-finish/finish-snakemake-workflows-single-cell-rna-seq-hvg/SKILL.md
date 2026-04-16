---
name: finish-snakemake-workflows-single-cell-rna-seq-hvg
description: Use this skill when orchestrating the retained "hvg" step of the snakemake workflows single cell rna seq finish finish workflow. It keeps the hvg stage tied to upstream `batch_effect_removal` and the downstream handoff to `correlation`. It tracks completion via `results/finish/hvg.done`.
metadata:
  workflow_id: single-cell-rna-seq-finish
  workflow_name: snakemake workflows single cell rna seq finish
  step_id: hvg
  step_name: hvg
---

# Scope
Use this skill only for the `hvg` step in `single-cell-rna-seq-finish`.

## Orchestration
- Upstream requirements: `batch_effect_removal`
- Step file: `finish/single-cell-rna-seq-finish/steps/hvg.smk`
- Config file: `finish/single-cell-rna-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/hvg.done`
- Representative outputs: `results/finish/hvg.done`
- Execution targets: `hvg`
- Downstream handoff: `correlation`

## Guardrails
- Treat `results/finish/hvg.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/hvg.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `correlation` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/hvg.done` exists and `correlation` can proceed without re-running hvg.
