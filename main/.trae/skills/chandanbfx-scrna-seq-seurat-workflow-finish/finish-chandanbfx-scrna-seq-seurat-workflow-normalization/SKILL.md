---
name: finish-chandanbfx-scrna-seq-seurat-workflow-normalization
description: Use this skill when orchestrating the retained "normalization" step of the chandanbfx scrna seq seurat workflow finish finish workflow. It keeps the normalization stage tied to upstream `qc` and the downstream handoff to `batch_correction`. It tracks completion via `results/finish/normalization.done`.
metadata:
  workflow_id: chandanbfx-scrna-seq-seurat-workflow-finish
  workflow_name: chandanbfx scrna seq seurat workflow finish
  step_id: normalization
  step_name: normalization
---

# Scope
Use this skill only for the `normalization` step in `chandanbfx-scrna-seq-seurat-workflow-finish`.

## Orchestration
- Upstream requirements: `qc`
- Step file: `finish/chandanbfx-scrna-seq-seurat-workflow-finish/steps/normalization.smk`
- Config file: `finish/chandanbfx-scrna-seq-seurat-workflow-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/normalization.done`
- Representative outputs: `results/finish/normalization.done`
- Execution targets: `normalization`
- Downstream handoff: `batch_correction`

## Guardrails
- Treat `results/finish/normalization.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/normalization.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `batch_correction` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/normalization.done` exists and `batch_correction` can proceed without re-running normalization.
