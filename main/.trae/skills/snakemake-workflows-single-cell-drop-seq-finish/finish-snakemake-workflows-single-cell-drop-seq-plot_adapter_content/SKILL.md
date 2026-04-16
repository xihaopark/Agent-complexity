---
name: finish-snakemake-workflows-single-cell-drop-seq-plot_adapter_content
description: Use this skill when orchestrating the retained "plot_adapter_content" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the plot adapter content stage tied to upstream `detect_barcodes` and the downstream handoff to `multiqc_cutadapt_barcodes`. It tracks completion via `results/finish/plot_adapter_content.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: plot_adapter_content
  step_name: plot adapter content
---

# Scope
Use this skill only for the `plot_adapter_content` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `detect_barcodes`
- Step file: `finish/single-cell-drop-seq-finish/steps/plot_adapter_content.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plot_adapter_content.done`
- Representative outputs: `results/finish/plot_adapter_content.done`
- Execution targets: `plot_adapter_content`
- Downstream handoff: `multiqc_cutadapt_barcodes`

## Guardrails
- Treat `results/finish/plot_adapter_content.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plot_adapter_content.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `multiqc_cutadapt_barcodes` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plot_adapter_content.done` exists and `multiqc_cutadapt_barcodes` can proceed without re-running plot adapter content.
