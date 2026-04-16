---
name: finish-epigen-scrnaseq-processing-seurat-correct
description: Use this skill when orchestrating the retained "correct" step of the epigen scrnaseq_processing_seurat finish finish workflow. It keeps the correct stage tied to upstream `normalize` and the downstream handoff to `metadata_plots`. It tracks completion via `results/finish/correct.done`.
metadata:
  workflow_id: epigen-scrnaseq_processing_seurat-finish
  workflow_name: epigen scrnaseq_processing_seurat finish
  step_id: correct
  step_name: correct
---

# Scope
Use this skill only for the `correct` step in `epigen-scrnaseq_processing_seurat-finish`.

## Orchestration
- Upstream requirements: `normalize`
- Step file: `finish/epigen-scrnaseq_processing_seurat-finish/steps/correct.smk`
- Config file: `finish/epigen-scrnaseq_processing_seurat-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/correct.done`
- Representative outputs: `results/finish/correct.done`
- Execution targets: `correct`
- Downstream handoff: `metadata_plots`

## Guardrails
- Treat `results/finish/correct.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/correct.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `metadata_plots` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/correct.done` exists and `metadata_plots` can proceed without re-running correct.
