---
name: finish-snakemake-workflows-single-cell-drop-seq-multiqc_cutadapt_barcodes
description: Use this skill when orchestrating the retained "multiqc_cutadapt_barcodes" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the multiqc cutadapt barcodes stage tied to upstream `plot_adapter_content` and the downstream handoff to `multiqc_cutadapt_RNA`. It tracks completion via `results/finish/multiqc_cutadapt_barcodes.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: multiqc_cutadapt_barcodes
  step_name: multiqc cutadapt barcodes
---

# Scope
Use this skill only for the `multiqc_cutadapt_barcodes` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `plot_adapter_content`
- Step file: `finish/single-cell-drop-seq-finish/steps/multiqc_cutadapt_barcodes.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/multiqc_cutadapt_barcodes.done`
- Representative outputs: `results/finish/multiqc_cutadapt_barcodes.done`
- Execution targets: `multiqc_cutadapt_barcodes`
- Downstream handoff: `multiqc_cutadapt_RNA`

## Guardrails
- Treat `results/finish/multiqc_cutadapt_barcodes.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/multiqc_cutadapt_barcodes.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `multiqc_cutadapt_RNA` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/multiqc_cutadapt_barcodes.done` exists and `multiqc_cutadapt_RNA` can proceed without re-running multiqc cutadapt barcodes.
