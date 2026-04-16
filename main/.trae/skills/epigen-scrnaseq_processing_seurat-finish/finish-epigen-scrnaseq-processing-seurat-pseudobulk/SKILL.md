---
name: finish-epigen-scrnaseq-processing-seurat-pseudobulk
description: Use this skill when orchestrating the retained "pseudobulk" step of the epigen scrnaseq_processing_seurat finish finish workflow. It keeps the pseudobulk stage tied to upstream `filter_cells` and the downstream handoff to `save_counts`. It tracks completion via `results/finish/pseudobulk.done`.
metadata:
  workflow_id: epigen-scrnaseq_processing_seurat-finish
  workflow_name: epigen scrnaseq_processing_seurat finish
  step_id: pseudobulk
  step_name: pseudobulk
---

# Scope
Use this skill only for the `pseudobulk` step in `epigen-scrnaseq_processing_seurat-finish`.

## Orchestration
- Upstream requirements: `filter_cells`
- Step file: `finish/epigen-scrnaseq_processing_seurat-finish/steps/pseudobulk.smk`
- Config file: `finish/epigen-scrnaseq_processing_seurat-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/pseudobulk.done`
- Representative outputs: `results/finish/pseudobulk.done`
- Execution targets: `pseudobulk`
- Downstream handoff: `save_counts`

## Guardrails
- Treat `results/finish/pseudobulk.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/pseudobulk.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `save_counts` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/pseudobulk.done` exists and `save_counts` can proceed without re-running pseudobulk.
