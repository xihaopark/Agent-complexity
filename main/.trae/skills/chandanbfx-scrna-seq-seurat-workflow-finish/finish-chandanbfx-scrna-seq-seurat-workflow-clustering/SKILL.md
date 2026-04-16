---
name: finish-chandanbfx-scrna-seq-seurat-workflow-clustering
description: Use this skill when orchestrating the retained "clustering" step of the chandanbfx scrna seq seurat workflow finish finish workflow. It keeps the clustering stage tied to upstream `dimreduction` and the downstream handoff to `marker_genes`. It tracks completion via `results/finish/clustering.done`.
metadata:
  workflow_id: chandanbfx-scrna-seq-seurat-workflow-finish
  workflow_name: chandanbfx scrna seq seurat workflow finish
  step_id: clustering
  step_name: clustering
---

# Scope
Use this skill only for the `clustering` step in `chandanbfx-scrna-seq-seurat-workflow-finish`.

## Orchestration
- Upstream requirements: `dimreduction`
- Step file: `finish/chandanbfx-scrna-seq-seurat-workflow-finish/steps/clustering.smk`
- Config file: `finish/chandanbfx-scrna-seq-seurat-workflow-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/clustering.done`
- Representative outputs: `results/finish/clustering.done`
- Execution targets: `clustering`
- Downstream handoff: `marker_genes`

## Guardrails
- Treat `results/finish/clustering.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/clustering.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `marker_genes` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/clustering.done` exists and `marker_genes` can proceed without re-running clustering.
