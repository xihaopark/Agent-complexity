---
name: finish-snakemake-workflows-single-cell-drop-seq-qc
description: Use this skill when orchestrating the retained "qc" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the qc stage tied to upstream `download_meta` and the downstream handoff to `filter`. It tracks completion via `results/finish/qc.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: qc
  step_name: qc
---

# Scope
Use this skill only for the `qc` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `download_meta`
- Step file: `finish/single-cell-drop-seq-finish/steps/qc.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/qc.done`
- Representative outputs: `results/finish/qc.done`
- Execution targets: `qc`
- Downstream handoff: `filter`

## Guardrails
- Treat `results/finish/qc.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/qc.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `filter` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/qc.done` exists and `filter` can proceed without re-running qc.
