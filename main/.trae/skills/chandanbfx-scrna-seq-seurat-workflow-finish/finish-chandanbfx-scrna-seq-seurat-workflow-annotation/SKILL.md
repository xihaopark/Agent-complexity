---
name: finish-chandanbfx-scrna-seq-seurat-workflow-annotation
description: Use this skill when orchestrating the retained "annotation" step of the chandanbfx scrna seq seurat workflow finish finish workflow. It keeps the annotation stage tied to upstream `marker_genes` and the downstream handoff to `generate_summary`. It tracks completion via `results/finish/annotation.done`.
metadata:
  workflow_id: chandanbfx-scrna-seq-seurat-workflow-finish
  workflow_name: chandanbfx scrna seq seurat workflow finish
  step_id: annotation
  step_name: annotation
---

# Scope
Use this skill only for the `annotation` step in `chandanbfx-scrna-seq-seurat-workflow-finish`.

## Orchestration
- Upstream requirements: `marker_genes`
- Step file: `finish/chandanbfx-scrna-seq-seurat-workflow-finish/steps/annotation.smk`
- Config file: `finish/chandanbfx-scrna-seq-seurat-workflow-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/annotation.done`
- Representative outputs: `results/finish/annotation.done`
- Execution targets: `annotation`
- Downstream handoff: `generate_summary`

## Guardrails
- Treat `results/finish/annotation.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/annotation.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `generate_summary` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/annotation.done` exists and `generate_summary` can proceed without re-running annotation.
