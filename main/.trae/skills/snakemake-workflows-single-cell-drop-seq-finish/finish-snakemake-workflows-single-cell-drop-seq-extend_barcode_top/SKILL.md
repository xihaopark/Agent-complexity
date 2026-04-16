---
name: finish-snakemake-workflows-single-cell-drop-seq-extend_barcode_top
description: Use this skill when orchestrating the retained "extend_barcode_top" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the extend barcode top stage tied to upstream `get_cell_whitelist` and the downstream handoff to `repair_barcodes`. It tracks completion via `results/finish/extend_barcode_top.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: extend_barcode_top
  step_name: extend barcode top
---

# Scope
Use this skill only for the `extend_barcode_top` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `get_cell_whitelist`
- Step file: `finish/single-cell-drop-seq-finish/steps/extend_barcode_top.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/extend_barcode_top.done`
- Representative outputs: `results/finish/extend_barcode_top.done`
- Execution targets: `extend_barcode_top`
- Downstream handoff: `repair_barcodes`

## Guardrails
- Treat `results/finish/extend_barcode_top.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/extend_barcode_top.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `repair_barcodes` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/extend_barcode_top.done` exists and `repair_barcodes` can proceed without re-running extend barcode top.
