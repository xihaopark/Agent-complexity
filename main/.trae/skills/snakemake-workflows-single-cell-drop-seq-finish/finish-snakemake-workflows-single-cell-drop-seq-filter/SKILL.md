---
name: finish-snakemake-workflows-single-cell-drop-seq-filter
description: Use this skill when orchestrating the retained "filter" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the filter stage tied to upstream `qc` and the downstream handoff to `map`. It tracks completion via `results/finish/filter.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: filter
  step_name: filter
---

# Scope
Use this skill only for the `filter` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `qc`
- Step file: `finish/single-cell-drop-seq-finish/steps/filter.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/filter.done`
- Representative outputs: `results/finish/filter.done`
- Execution targets: `filter`
- Downstream handoff: `map`

## Guardrails
- Treat `results/finish/filter.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/filter.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `map` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/filter.done` exists and `map` can proceed without re-running filter.
