---
name: finish-epigen-scrnaseq-processing-seurat-filter_cells
description: Use this skill when orchestrating the retained "filter_cells" step of the epigen scrnaseq_processing_seurat finish finish workflow. It keeps the filter cells stage tied to upstream `split` and the downstream handoff to `pseudobulk`. It tracks completion via `results/finish/filter_cells.done`.
metadata:
  workflow_id: epigen-scrnaseq_processing_seurat-finish
  workflow_name: epigen scrnaseq_processing_seurat finish
  step_id: filter_cells
  step_name: filter cells
---

# Scope
Use this skill only for the `filter_cells` step in `epigen-scrnaseq_processing_seurat-finish`.

## Orchestration
- Upstream requirements: `split`
- Step file: `finish/epigen-scrnaseq_processing_seurat-finish/steps/filter_cells.smk`
- Config file: `finish/epigen-scrnaseq_processing_seurat-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/filter_cells.done`
- Representative outputs: `results/finish/filter_cells.done`
- Execution targets: `filter_cells`
- Downstream handoff: `pseudobulk`

## Guardrails
- Treat `results/finish/filter_cells.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/filter_cells.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `pseudobulk` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/filter_cells.done` exists and `pseudobulk` can proceed without re-running filter cells.
