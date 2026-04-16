---
name: finish-snakemake-workflows-single-cell-drop-seq-get_top_barcodes
description: Use this skill when orchestrating the retained "get_top_barcodes" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the get top barcodes stage tied to upstream `extend_barcode_whitelist` and the downstream handoff to `get_cell_whitelist`. It tracks completion via `results/finish/get_top_barcodes.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: get_top_barcodes
  step_name: get top barcodes
---

# Scope
Use this skill only for the `get_top_barcodes` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `extend_barcode_whitelist`
- Step file: `finish/single-cell-drop-seq-finish/steps/get_top_barcodes.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_top_barcodes.done`
- Representative outputs: `results/finish/get_top_barcodes.done`
- Execution targets: `get_top_barcodes`
- Downstream handoff: `get_cell_whitelist`

## Guardrails
- Treat `results/finish/get_top_barcodes.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_top_barcodes.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `get_cell_whitelist` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_top_barcodes.done` exists and `get_cell_whitelist` can proceed without re-running get top barcodes.
