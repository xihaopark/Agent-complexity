---
name: finish-snakemake-workflows-single-cell-drop-seq-map
description: Use this skill when orchestrating the retained "map" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the map stage tied to upstream `filter` and the downstream handoff to `extract`. It tracks completion via `results/finish/map.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: map
  step_name: map
---

# Scope
Use this skill only for the `map` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `filter`
- Step file: `finish/single-cell-drop-seq-finish/steps/map.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/map.done`
- Representative outputs: `results/finish/map.done`
- Execution targets: `map`
- Downstream handoff: `extract`

## Guardrails
- Treat `results/finish/map.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/map.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `extract` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/map.done` exists and `extract` can proceed without re-running map.
