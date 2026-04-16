---
name: finish-chandanbfx-scrna-seq-seurat-workflow-batch_correction
description: Use this skill when orchestrating the retained "batch_correction" step of the chandanbfx scrna seq seurat workflow finish finish workflow. It keeps the batch correction stage tied to upstream `normalization` and the downstream handoff to `dimreduction`. It tracks completion via `results/finish/batch_correction.done`.
metadata:
  workflow_id: chandanbfx-scrna-seq-seurat-workflow-finish
  workflow_name: chandanbfx scrna seq seurat workflow finish
  step_id: batch_correction
  step_name: batch correction
---

# Scope
Use this skill only for the `batch_correction` step in `chandanbfx-scrna-seq-seurat-workflow-finish`.

## Orchestration
- Upstream requirements: `normalization`
- Step file: `finish/chandanbfx-scrna-seq-seurat-workflow-finish/steps/batch_correction.smk`
- Config file: `finish/chandanbfx-scrna-seq-seurat-workflow-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/batch_correction.done`
- Representative outputs: `results/finish/batch_correction.done`
- Execution targets: `batch_correction`
- Downstream handoff: `dimreduction`

## Guardrails
- Treat `results/finish/batch_correction.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/batch_correction.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `dimreduction` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/batch_correction.done` exists and `dimreduction` can proceed without re-running batch correction.
