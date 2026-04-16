---
name: finish-epigen-scrnaseq-processing-seurat-metadata_plots
description: Use this skill when orchestrating the retained "metadata_plots" step of the epigen scrnaseq_processing_seurat finish finish workflow. It keeps the metadata plots stage tied to upstream `correct` and the downstream handoff to `seurat_plots`. It tracks completion via `results/finish/metadata_plots.done`.
metadata:
  workflow_id: epigen-scrnaseq_processing_seurat-finish
  workflow_name: epigen scrnaseq_processing_seurat finish
  step_id: metadata_plots
  step_name: metadata plots
---

# Scope
Use this skill only for the `metadata_plots` step in `epigen-scrnaseq_processing_seurat-finish`.

## Orchestration
- Upstream requirements: `correct`
- Step file: `finish/epigen-scrnaseq_processing_seurat-finish/steps/metadata_plots.smk`
- Config file: `finish/epigen-scrnaseq_processing_seurat-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/metadata_plots.done`
- Representative outputs: `results/finish/metadata_plots.done`
- Execution targets: `metadata_plots`
- Downstream handoff: `seurat_plots`

## Guardrails
- Treat `results/finish/metadata_plots.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/metadata_plots.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `seurat_plots` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/metadata_plots.done` exists and `seurat_plots` can proceed without re-running metadata plots.
