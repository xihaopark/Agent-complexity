---
name: finish-epigen-dea-seurat-volcanos
description: Use this skill when orchestrating the retained "volcanos" step of the epigen dea_seurat finish finish workflow. It keeps the volcanos stage tied to upstream `feature_lists` and the downstream handoff to `heatmap`. It tracks completion via `results/finish/volcanos.done`.
metadata:
  workflow_id: epigen-dea_seurat-finish
  workflow_name: epigen dea_seurat finish
  step_id: volcanos
  step_name: volcanos
---

# Scope
Use this skill only for the `volcanos` step in `epigen-dea_seurat-finish`.

## Orchestration
- Upstream requirements: `feature_lists`
- Step file: `finish/epigen-dea_seurat-finish/steps/volcanos.smk`
- Config file: `finish/epigen-dea_seurat-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/volcanos.done`
- Representative outputs: `results/finish/volcanos.done`
- Execution targets: `volcanos`
- Downstream handoff: `heatmap`

## Guardrails
- Treat `results/finish/volcanos.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/volcanos.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `heatmap` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/volcanos.done` exists and `heatmap` can proceed without re-running volcanos.
