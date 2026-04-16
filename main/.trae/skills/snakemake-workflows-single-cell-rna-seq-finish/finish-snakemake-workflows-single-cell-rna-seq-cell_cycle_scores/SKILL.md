---
name: finish-snakemake-workflows-single-cell-rna-seq-cell_cycle_scores
description: Use this skill when orchestrating the retained "cell_cycle_scores" step of the snakemake workflows single cell rna seq finish finish workflow. It keeps the cell cycle scores stage tied to upstream `cell_cycle` and the downstream handoff to `normalize`. It tracks completion via `results/finish/cell_cycle_scores.done`.
metadata:
  workflow_id: single-cell-rna-seq-finish
  workflow_name: snakemake workflows single cell rna seq finish
  step_id: cell_cycle_scores
  step_name: cell cycle scores
---

# Scope
Use this skill only for the `cell_cycle_scores` step in `single-cell-rna-seq-finish`.

## Orchestration
- Upstream requirements: `cell_cycle`
- Step file: `finish/single-cell-rna-seq-finish/steps/cell_cycle_scores.smk`
- Config file: `finish/single-cell-rna-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/cell_cycle_scores.done`
- Representative outputs: `results/finish/cell_cycle_scores.done`
- Execution targets: `cell_cycle_scores`
- Downstream handoff: `normalize`

## Guardrails
- Treat `results/finish/cell_cycle_scores.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/cell_cycle_scores.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `normalize` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/cell_cycle_scores.done` exists and `normalize` can proceed without re-running cell cycle scores.
