---
name: finish-snakemake-workflows-single-cell-drop-seq-get_cell_whitelist
description: Use this skill when orchestrating the retained "get_cell_whitelist" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the get cell whitelist stage tied to upstream `get_top_barcodes` and the downstream handoff to `extend_barcode_top`. It tracks completion via `results/finish/get_cell_whitelist.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: get_cell_whitelist
  step_name: get cell whitelist
---

# Scope
Use this skill only for the `get_cell_whitelist` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `get_top_barcodes`
- Step file: `finish/single-cell-drop-seq-finish/steps/get_cell_whitelist.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_cell_whitelist.done`
- Representative outputs: `results/finish/get_cell_whitelist.done`
- Execution targets: `get_cell_whitelist`
- Downstream handoff: `extend_barcode_top`

## Guardrails
- Treat `results/finish/get_cell_whitelist.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_cell_whitelist.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `extend_barcode_top` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_cell_whitelist.done` exists and `extend_barcode_top` can proceed without re-running get cell whitelist.
