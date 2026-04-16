---
name: finish-epigen-scrnaseq-processing-seurat-seurat_plots
description: Use this skill when orchestrating the retained "seurat_plots" step of the epigen scrnaseq_processing_seurat finish finish workflow. It keeps the seurat plots stage tied to upstream `metadata_plots` and the downstream handoff to `env_export`. It tracks completion via `results/finish/seurat_plots.done`.
metadata:
  workflow_id: epigen-scrnaseq_processing_seurat-finish
  workflow_name: epigen scrnaseq_processing_seurat finish
  step_id: seurat_plots
  step_name: seurat plots
---

# Scope
Use this skill only for the `seurat_plots` step in `epigen-scrnaseq_processing_seurat-finish`.

## Orchestration
- Upstream requirements: `metadata_plots`
- Step file: `finish/epigen-scrnaseq_processing_seurat-finish/steps/seurat_plots.smk`
- Config file: `finish/epigen-scrnaseq_processing_seurat-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/seurat_plots.done`
- Representative outputs: `results/finish/seurat_plots.done`
- Execution targets: `seurat_plots`
- Downstream handoff: `env_export`

## Guardrails
- Treat `results/finish/seurat_plots.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/seurat_plots.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `env_export` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/seurat_plots.done` exists and `env_export` can proceed without re-running seurat plots.
