---
name: finish-snakemake-workflows-single-cell-drop-seq-create_intervals
description: Use this skill when orchestrating the retained "create_intervals" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the create intervals stage tied to upstream `create_refFlat` and the downstream handoff to `get_genomeChrBinNbits`. It tracks completion via `results/finish/create_intervals.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: create_intervals
  step_name: create intervals
---

# Scope
Use this skill only for the `create_intervals` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `create_refFlat`
- Step file: `finish/single-cell-drop-seq-finish/steps/create_intervals.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/create_intervals.done`
- Representative outputs: `results/finish/create_intervals.done`
- Execution targets: `create_intervals`
- Downstream handoff: `get_genomeChrBinNbits`

## Guardrails
- Treat `results/finish/create_intervals.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/create_intervals.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `get_genomeChrBinNbits` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/create_intervals.done` exists and `get_genomeChrBinNbits` can proceed without re-running create intervals.
