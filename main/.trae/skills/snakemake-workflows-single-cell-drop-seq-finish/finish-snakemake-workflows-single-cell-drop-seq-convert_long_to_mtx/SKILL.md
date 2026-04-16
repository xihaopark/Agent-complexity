---
name: finish-snakemake-workflows-single-cell-drop-seq-convert_long_to_mtx
description: Use this skill when orchestrating the retained "convert_long_to_mtx" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the convert long to mtx stage tied to upstream `plot_rna_metrics` and the downstream handoff to `compress_mtx`. It tracks completion via `results/finish/convert_long_to_mtx.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: convert_long_to_mtx
  step_name: convert long to mtx
---

# Scope
Use this skill only for the `convert_long_to_mtx` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `plot_rna_metrics`
- Step file: `finish/single-cell-drop-seq-finish/steps/convert_long_to_mtx.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/convert_long_to_mtx.done`
- Representative outputs: `results/finish/convert_long_to_mtx.done`
- Execution targets: `convert_long_to_mtx`
- Downstream handoff: `compress_mtx`

## Guardrails
- Treat `results/finish/convert_long_to_mtx.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/convert_long_to_mtx.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `compress_mtx` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/convert_long_to_mtx.done` exists and `compress_mtx` can proceed without re-running convert long to mtx.
