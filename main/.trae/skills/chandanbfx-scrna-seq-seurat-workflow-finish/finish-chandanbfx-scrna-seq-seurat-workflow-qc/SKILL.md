---
name: finish-chandanbfx-scrna-seq-seurat-workflow-qc
description: Use this skill when orchestrating the retained "qc" step of the chandanbfx scrna seq seurat workflow finish finish workflow. It keeps the qc stage tied to upstream `create_seurat_object` and the downstream handoff to `normalization`. It tracks completion via `results/finish/qc.done`.
metadata:
  workflow_id: chandanbfx-scrna-seq-seurat-workflow-finish
  workflow_name: chandanbfx scrna seq seurat workflow finish
  step_id: qc
  step_name: qc
---

# Scope
Use this skill only for the `qc` step in `chandanbfx-scrna-seq-seurat-workflow-finish`.

## Orchestration
- Upstream requirements: `create_seurat_object`
- Step file: `finish/chandanbfx-scrna-seq-seurat-workflow-finish/steps/qc.smk`
- Config file: `finish/chandanbfx-scrna-seq-seurat-workflow-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/qc.done`
- Representative outputs: `results/finish/qc.done`
- Execution targets: `qc`
- Downstream handoff: `normalization`

## Guardrails
- Treat `results/finish/qc.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/qc.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `normalization` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/qc.done` exists and `normalization` can proceed without re-running qc.
