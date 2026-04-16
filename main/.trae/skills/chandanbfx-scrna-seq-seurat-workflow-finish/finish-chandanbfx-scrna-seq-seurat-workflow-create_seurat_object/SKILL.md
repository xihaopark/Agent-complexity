---
name: finish-chandanbfx-scrna-seq-seurat-workflow-create_seurat_object
description: Use this skill when orchestrating the retained "create_seurat_object" step of the chandanbfx scrna seq seurat workflow finish finish workflow. It keeps the create seurat object stage and the downstream handoff to `qc`. It tracks completion via `results/finish/create_seurat_object.done`.
metadata:
  workflow_id: chandanbfx-scrna-seq-seurat-workflow-finish
  workflow_name: chandanbfx scrna seq seurat workflow finish
  step_id: create_seurat_object
  step_name: create seurat object
---

# Scope
Use this skill only for the `create_seurat_object` step in `chandanbfx-scrna-seq-seurat-workflow-finish`.

## Orchestration
- Upstream requirements: none
- Step file: `finish/chandanbfx-scrna-seq-seurat-workflow-finish/steps/create_seurat_object.smk`
- Config file: `finish/chandanbfx-scrna-seq-seurat-workflow-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/create_seurat_object.done`
- Representative outputs: `results/finish/create_seurat_object.done`
- Execution targets: `create_seurat_object`
- Downstream handoff: `qc`

## Guardrails
- Treat `results/finish/create_seurat_object.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/create_seurat_object.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `qc` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/create_seurat_object.done` exists and `qc` can proceed without re-running create seurat object.
