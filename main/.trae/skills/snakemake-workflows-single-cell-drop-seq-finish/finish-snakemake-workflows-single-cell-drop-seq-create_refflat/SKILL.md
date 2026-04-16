---
name: finish-snakemake-workflows-single-cell-drop-seq-create_refflat
description: Use this skill when orchestrating the retained "create_refFlat" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the create refFlat stage tied to upstream `reduce_gtf` and the downstream handoff to `create_intervals`. It tracks completion via `results/finish/create_refFlat.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: create_refFlat
  step_name: create refFlat
---

# Scope
Use this skill only for the `create_refFlat` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `reduce_gtf`
- Step file: `finish/single-cell-drop-seq-finish/steps/create_refFlat.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/create_refFlat.done`
- Representative outputs: `results/finish/create_refFlat.done`
- Execution targets: `create_refFlat`
- Downstream handoff: `create_intervals`

## Guardrails
- Treat `results/finish/create_refFlat.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/create_refFlat.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `create_intervals` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/create_refFlat.done` exists and `create_intervals` can proceed without re-running create refFlat.
