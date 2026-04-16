---
name: finish-snakemake-workflows-single-cell-rna-seq-normalize
description: Use this skill when orchestrating the retained "normalize" step of the snakemake workflows single cell rna seq finish finish workflow. It keeps the normalize stage tied to upstream `cell_cycle_scores` and the downstream handoff to `batch_effect_removal`. It tracks completion via `results/finish/normalize.done`.
metadata:
  workflow_id: single-cell-rna-seq-finish
  workflow_name: snakemake workflows single cell rna seq finish
  step_id: normalize
  step_name: normalize
---

# Scope
Use this skill only for the `normalize` step in `single-cell-rna-seq-finish`.

## Orchestration
- Upstream requirements: `cell_cycle_scores`
- Step file: `finish/single-cell-rna-seq-finish/steps/normalize.smk`
- Config file: `finish/single-cell-rna-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/normalize.done`
- Representative outputs: `results/finish/normalize.done`
- Execution targets: `normalize`
- Downstream handoff: `batch_effect_removal`

## Guardrails
- Treat `results/finish/normalize.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/normalize.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `batch_effect_removal` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/normalize.done` exists and `batch_effect_removal` can proceed without re-running normalize.
