---
name: finish-epigen-scrnaseq-processing-seurat-save_counts
description: Use this skill when orchestrating the retained "save_counts" step of the epigen scrnaseq_processing_seurat finish finish workflow. It keeps the save counts stage tied to upstream `pseudobulk` and the downstream handoff to `normalize`. It tracks completion via `results/finish/save_counts.done`.
metadata:
  workflow_id: epigen-scrnaseq_processing_seurat-finish
  workflow_name: epigen scrnaseq_processing_seurat finish
  step_id: save_counts
  step_name: save counts
---

# Scope
Use this skill only for the `save_counts` step in `epigen-scrnaseq_processing_seurat-finish`.

## Orchestration
- Upstream requirements: `pseudobulk`
- Step file: `finish/epigen-scrnaseq_processing_seurat-finish/steps/save_counts.smk`
- Config file: `finish/epigen-scrnaseq_processing_seurat-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/save_counts.done`
- Representative outputs: `results/finish/save_counts.done`
- Execution targets: `save_counts`
- Downstream handoff: `normalize`

## Guardrails
- Treat `results/finish/save_counts.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/save_counts.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `normalize` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/save_counts.done` exists and `normalize` can proceed without re-running save counts.
