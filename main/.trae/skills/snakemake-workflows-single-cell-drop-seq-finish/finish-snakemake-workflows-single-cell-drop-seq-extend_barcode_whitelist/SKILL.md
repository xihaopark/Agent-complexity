---
name: finish-snakemake-workflows-single-cell-drop-seq-extend_barcode_whitelist
description: Use this skill when orchestrating the retained "extend_barcode_whitelist" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the extend barcode whitelist stage tied to upstream `multiqc_cutadapt_RNA` and the downstream handoff to `get_top_barcodes`. It tracks completion via `results/finish/extend_barcode_whitelist.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: extend_barcode_whitelist
  step_name: extend barcode whitelist
---

# Scope
Use this skill only for the `extend_barcode_whitelist` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `multiqc_cutadapt_RNA`
- Step file: `finish/single-cell-drop-seq-finish/steps/extend_barcode_whitelist.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/extend_barcode_whitelist.done`
- Representative outputs: `results/finish/extend_barcode_whitelist.done`
- Execution targets: `extend_barcode_whitelist`
- Downstream handoff: `get_top_barcodes`

## Guardrails
- Treat `results/finish/extend_barcode_whitelist.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/extend_barcode_whitelist.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `get_top_barcodes` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/extend_barcode_whitelist.done` exists and `get_top_barcodes` can proceed without re-running extend barcode whitelist.
