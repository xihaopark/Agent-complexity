---
name: finish-snakemake-workflows-single-cell-drop-seq-repair_barcodes
description: Use this skill when orchestrating the retained "repair_barcodes" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the repair barcodes stage tied to upstream `extend_barcode_top` and the downstream handoff to `STAR_align`. It tracks completion via `results/finish/repair_barcodes.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: repair_barcodes
  step_name: repair barcodes
---

# Scope
Use this skill only for the `repair_barcodes` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `extend_barcode_top`
- Step file: `finish/single-cell-drop-seq-finish/steps/repair_barcodes.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/repair_barcodes.done`
- Representative outputs: `results/finish/repair_barcodes.done`
- Execution targets: `repair_barcodes`
- Downstream handoff: `STAR_align`

## Guardrails
- Treat `results/finish/repair_barcodes.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/repair_barcodes.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `STAR_align` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/repair_barcodes.done` exists and `STAR_align` can proceed without re-running repair barcodes.
