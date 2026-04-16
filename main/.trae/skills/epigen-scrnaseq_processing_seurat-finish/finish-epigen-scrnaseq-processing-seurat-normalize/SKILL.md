---
name: finish-epigen-scrnaseq-processing-seurat-normalize
description: Use this skill when orchestrating the retained "normalize" step of the epigen scrnaseq_processing_seurat finish finish workflow. It keeps the normalize stage tied to upstream `save_counts` and the downstream handoff to `correct`. It tracks completion via `results/finish/normalize.done`.
metadata:
  workflow_id: epigen-scrnaseq_processing_seurat-finish
  workflow_name: epigen scrnaseq_processing_seurat finish
  step_id: normalize
  step_name: normalize
---

# Scope
Use this skill only for the `normalize` step in `epigen-scrnaseq_processing_seurat-finish`.

## Orchestration
- Upstream requirements: `save_counts`
- Step file: `finish/epigen-scrnaseq_processing_seurat-finish/steps/normalize.smk`
- Config file: `finish/epigen-scrnaseq_processing_seurat-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/normalize.done`
- Representative outputs: `results/finish/normalize.done`
- Execution targets: `normalize`
- Downstream handoff: `correct`

## Guardrails
- Treat `results/finish/normalize.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/normalize.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `correct` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/normalize.done` exists and `correct` can proceed without re-running normalize.
