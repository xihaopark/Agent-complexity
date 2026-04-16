---
name: finish-snakemake-workflows-single-cell-drop-seq-download_meta
description: Use this skill when orchestrating the retained "download_meta" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the download meta stage and the downstream handoff to `qc`. It tracks completion via `results/finish/download_meta.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: download_meta
  step_name: download meta
---

# Scope
Use this skill only for the `download_meta` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: none
- Step file: `finish/single-cell-drop-seq-finish/steps/download_meta.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/download_meta.done`
- Representative outputs: `results/finish/download_meta.done`
- Execution targets: `download_meta`
- Downstream handoff: `qc`

## Guardrails
- Treat `results/finish/download_meta.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/download_meta.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `qc` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/download_meta.done` exists and `qc` can proceed without re-running download meta.
