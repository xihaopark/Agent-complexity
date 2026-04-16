---
name: finish-chandanbfx-scrna-seq-seurat-workflow-marker_genes
description: Use this skill when orchestrating the retained "marker_genes" step of the chandanbfx scrna seq seurat workflow finish finish workflow. It keeps the marker genes stage tied to upstream `clustering` and the downstream handoff to `annotation`. It tracks completion via `results/finish/marker_genes.done`.
metadata:
  workflow_id: chandanbfx-scrna-seq-seurat-workflow-finish
  workflow_name: chandanbfx scrna seq seurat workflow finish
  step_id: marker_genes
  step_name: marker genes
---

# Scope
Use this skill only for the `marker_genes` step in `chandanbfx-scrna-seq-seurat-workflow-finish`.

## Orchestration
- Upstream requirements: `clustering`
- Step file: `finish/chandanbfx-scrna-seq-seurat-workflow-finish/steps/marker_genes.smk`
- Config file: `finish/chandanbfx-scrna-seq-seurat-workflow-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/marker_genes.done`
- Representative outputs: `results/finish/marker_genes.done`
- Execution targets: `marker_genes`
- Downstream handoff: `annotation`

## Guardrails
- Treat `results/finish/marker_genes.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/marker_genes.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `annotation` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/marker_genes.done` exists and `annotation` can proceed without re-running marker genes.
