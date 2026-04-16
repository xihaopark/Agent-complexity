---
name: finish-epigen-scrnaseq-processing-seurat-split
description: Use this skill when orchestrating the retained "split" step of the epigen scrnaseq_processing_seurat finish finish workflow. It keeps the split stage tied to upstream `merge` and the downstream handoff to `filter_cells`. It tracks completion via `results/finish/split.done`.
metadata:
  workflow_id: epigen-scrnaseq_processing_seurat-finish
  workflow_name: epigen scrnaseq_processing_seurat finish
  step_id: split
  step_name: split
---

# Scope
Use this skill only for the `split` step in `epigen-scrnaseq_processing_seurat-finish`.

## Orchestration
- Upstream requirements: `merge`
- Step file: `finish/epigen-scrnaseq_processing_seurat-finish/steps/split.smk`
- Config file: `finish/epigen-scrnaseq_processing_seurat-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/split.done`
- Representative outputs: `results/finish/split.done`
- Execution targets: `split`
- Downstream handoff: `filter_cells`

## Guardrails
- Treat `results/finish/split.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/split.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `filter_cells` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/split.done` exists and `filter_cells` can proceed without re-running split.
