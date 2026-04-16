---
name: finish-epigen-dea-seurat-feature_list_export
description: Use this skill when orchestrating the retained "feature_list_export" step of the epigen dea_seurat finish finish workflow. It keeps the feature list export stage tied to upstream `annot_export` and the downstream handoff to `all`. It tracks completion via `results/finish/feature_list_export.done`.
metadata:
  workflow_id: epigen-dea_seurat-finish
  workflow_name: epigen dea_seurat finish
  step_id: feature_list_export
  step_name: feature list export
---

# Scope
Use this skill only for the `feature_list_export` step in `epigen-dea_seurat-finish`.

## Orchestration
- Upstream requirements: `annot_export`
- Step file: `finish/epigen-dea_seurat-finish/steps/feature_list_export.smk`
- Config file: `finish/epigen-dea_seurat-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/feature_list_export.done`
- Representative outputs: `results/finish/feature_list_export.done`
- Execution targets: `feature_list_export`
- Downstream handoff: `all`

## Guardrails
- Treat `results/finish/feature_list_export.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/feature_list_export.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `all` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/feature_list_export.done` exists and `all` can proceed without re-running feature list export.
