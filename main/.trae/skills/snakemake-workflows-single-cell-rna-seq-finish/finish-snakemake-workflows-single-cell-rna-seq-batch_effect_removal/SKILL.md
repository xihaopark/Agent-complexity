---
name: finish-snakemake-workflows-single-cell-rna-seq-batch_effect_removal
description: Use this skill when orchestrating the retained "batch_effect_removal" step of the snakemake workflows single cell rna seq finish finish workflow. It keeps the batch effect removal stage tied to upstream `normalize` and the downstream handoff to `hvg`. It tracks completion via `results/finish/batch_effect_removal.done`.
metadata:
  workflow_id: single-cell-rna-seq-finish
  workflow_name: snakemake workflows single cell rna seq finish
  step_id: batch_effect_removal
  step_name: batch effect removal
---

# Scope
Use this skill only for the `batch_effect_removal` step in `single-cell-rna-seq-finish`.

## Orchestration
- Upstream requirements: `normalize`
- Step file: `finish/single-cell-rna-seq-finish/steps/batch_effect_removal.smk`
- Config file: `finish/single-cell-rna-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/batch_effect_removal.done`
- Representative outputs: `results/finish/batch_effect_removal.done`
- Execution targets: `batch_effect_removal`
- Downstream handoff: `hvg`

## Guardrails
- Treat `results/finish/batch_effect_removal.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/batch_effect_removal.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `hvg` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/batch_effect_removal.done` exists and `hvg` can proceed without re-running batch effect removal.
