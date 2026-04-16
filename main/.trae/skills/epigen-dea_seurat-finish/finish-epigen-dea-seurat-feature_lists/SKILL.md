---
name: finish-epigen-dea-seurat-feature_lists
description: Use this skill when orchestrating the retained "feature_lists" step of the epigen dea_seurat finish finish workflow. It keeps the feature lists stage tied to upstream `aggregate` and the downstream handoff to `volcanos`. It tracks completion via `results/finish/feature_lists.done`.
metadata:
  workflow_id: epigen-dea_seurat-finish
  workflow_name: epigen dea_seurat finish
  step_id: feature_lists
  step_name: feature lists
---

# Scope
Use this skill only for the `feature_lists` step in `epigen-dea_seurat-finish`.

## Orchestration
- Upstream requirements: `aggregate`
- Step file: `finish/epigen-dea_seurat-finish/steps/feature_lists.smk`
- Config file: `finish/epigen-dea_seurat-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/feature_lists.done`
- Representative outputs: `results/finish/feature_lists.done`
- Execution targets: `feature_lists`
- Downstream handoff: `volcanos`

## Guardrails
- Treat `results/finish/feature_lists.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/feature_lists.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `volcanos` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/feature_lists.done` exists and `volcanos` can proceed without re-running feature lists.
