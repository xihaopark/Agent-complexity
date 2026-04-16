---
name: finish-snakemake-workflows-single-cell-drop-seq-detect_barcodes
description: Use this skill when orchestrating the retained "detect_barcodes" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the detect barcodes stage tied to upstream `repair` and the downstream handoff to `plot_adapter_content`. It tracks completion via `results/finish/detect_barcodes.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: detect_barcodes
  step_name: detect barcodes
---

# Scope
Use this skill only for the `detect_barcodes` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `repair`
- Step file: `finish/single-cell-drop-seq-finish/steps/detect_barcodes.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/detect_barcodes.done`
- Representative outputs: `results/finish/detect_barcodes.done`
- Execution targets: `detect_barcodes`
- Downstream handoff: `plot_adapter_content`

## Guardrails
- Treat `results/finish/detect_barcodes.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/detect_barcodes.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plot_adapter_content` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/detect_barcodes.done` exists and `plot_adapter_content` can proceed without re-running detect barcodes.
