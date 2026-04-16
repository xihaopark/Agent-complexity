---
name: finish-snakemake-workflows-single-cell-drop-seq-multiqc_cutadapt_rna
description: Use this skill when orchestrating the retained "multiqc_cutadapt_RNA" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the multiqc cutadapt RNA stage tied to upstream `multiqc_cutadapt_barcodes` and the downstream handoff to `extend_barcode_whitelist`. It tracks completion via `results/finish/multiqc_cutadapt_RNA.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: multiqc_cutadapt_RNA
  step_name: multiqc cutadapt RNA
---

# Scope
Use this skill only for the `multiqc_cutadapt_RNA` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `multiqc_cutadapt_barcodes`
- Step file: `finish/single-cell-drop-seq-finish/steps/multiqc_cutadapt_RNA.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/multiqc_cutadapt_RNA.done`
- Representative outputs: `results/finish/multiqc_cutadapt_RNA.done`
- Execution targets: `multiqc_cutadapt_RNA`
- Downstream handoff: `extend_barcode_whitelist`

## Guardrails
- Treat `results/finish/multiqc_cutadapt_RNA.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/multiqc_cutadapt_RNA.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `extend_barcode_whitelist` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/multiqc_cutadapt_RNA.done` exists and `extend_barcode_whitelist` can proceed without re-running multiqc cutadapt RNA.
