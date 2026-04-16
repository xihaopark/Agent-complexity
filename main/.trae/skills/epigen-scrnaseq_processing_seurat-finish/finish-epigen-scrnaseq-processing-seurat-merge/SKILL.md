---
name: finish-epigen-scrnaseq-processing-seurat-merge
description: Use this skill when orchestrating the retained "merge" step of the epigen scrnaseq_processing_seurat finish finish workflow. It keeps the merge stage tied to upstream `prepare` and the downstream handoff to `split`. It tracks completion via `results/finish/merge.done`.
metadata:
  workflow_id: epigen-scrnaseq_processing_seurat-finish
  workflow_name: epigen scrnaseq_processing_seurat finish
  step_id: merge
  step_name: merge
---

# Scope
Use this skill only for the `merge` step in `epigen-scrnaseq_processing_seurat-finish`.

## Orchestration
- Upstream requirements: `prepare`
- Step file: `finish/epigen-scrnaseq_processing_seurat-finish/steps/merge.smk`
- Config file: `finish/epigen-scrnaseq_processing_seurat-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/merge.done`
- Representative outputs: `results/finish/merge.done`
- Execution targets: `merge`
- Downstream handoff: `split`

## Guardrails
- Treat `results/finish/merge.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/merge.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `split` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/merge.done` exists and `split` can proceed without re-running merge.
