---
name: finish-epigen-scrnaseq-processing-seurat-prepare
description: Use this skill when orchestrating the retained "prepare" step of the epigen scrnaseq_processing_seurat finish finish workflow. It keeps the prepare stage and the downstream handoff to `merge`. It tracks completion via `results/finish/prepare.done`.
metadata:
  workflow_id: epigen-scrnaseq_processing_seurat-finish
  workflow_name: epigen scrnaseq_processing_seurat finish
  step_id: prepare
  step_name: prepare
---

# Scope
Use this skill only for the `prepare` step in `epigen-scrnaseq_processing_seurat-finish`.

## Orchestration
- Upstream requirements: none
- Step file: `finish/epigen-scrnaseq_processing_seurat-finish/steps/prepare.smk`
- Config file: `finish/epigen-scrnaseq_processing_seurat-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/prepare.done`
- Representative outputs: `results/finish/prepare.done`
- Execution targets: `prepare`
- Downstream handoff: `merge`

## Guardrails
- Treat `results/finish/prepare.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/prepare.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `merge` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/prepare.done` exists and `merge` can proceed without re-running prepare.
