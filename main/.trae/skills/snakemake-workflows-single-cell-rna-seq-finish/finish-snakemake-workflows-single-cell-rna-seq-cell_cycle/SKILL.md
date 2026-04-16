---
name: finish-snakemake-workflows-single-cell-rna-seq-cell_cycle
description: Use this skill when orchestrating the retained "cell_cycle" step of the snakemake workflows single cell rna seq finish finish workflow. It keeps the cell cycle stage tied to upstream `filter_cells` and the downstream handoff to `cell_cycle_scores`. It tracks completion via `results/finish/cell_cycle.done`.
metadata:
  workflow_id: single-cell-rna-seq-finish
  workflow_name: snakemake workflows single cell rna seq finish
  step_id: cell_cycle
  step_name: cell cycle
---

# Scope
Use this skill only for the `cell_cycle` step in `single-cell-rna-seq-finish`.

## Orchestration
- Upstream requirements: `filter_cells`
- Step file: `finish/single-cell-rna-seq-finish/steps/cell_cycle.smk`
- Config file: `finish/single-cell-rna-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/cell_cycle.done`
- Representative outputs: `results/finish/cell_cycle.done`
- Execution targets: `cell_cycle`
- Downstream handoff: `cell_cycle_scores`

## Guardrails
- Treat `results/finish/cell_cycle.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/cell_cycle.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `cell_cycle_scores` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/cell_cycle.done` exists and `cell_cycle_scores` can proceed without re-running cell cycle.
