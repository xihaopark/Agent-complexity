---
name: finish-epigen-dea-seurat-heatmap
description: Use this skill when orchestrating the retained "heatmap" step of the epigen dea_seurat finish finish workflow. It keeps the heatmap stage tied to upstream `volcanos` and the downstream handoff to `env_export`. It tracks completion via `results/finish/heatmap.done`.
metadata:
  workflow_id: epigen-dea_seurat-finish
  workflow_name: epigen dea_seurat finish
  step_id: heatmap
  step_name: heatmap
---

# Scope
Use this skill only for the `heatmap` step in `epigen-dea_seurat-finish`.

## Orchestration
- Upstream requirements: `volcanos`
- Step file: `finish/epigen-dea_seurat-finish/steps/heatmap.smk`
- Config file: `finish/epigen-dea_seurat-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/heatmap.done`
- Representative outputs: `results/finish/heatmap.done`
- Execution targets: `heatmap`
- Downstream handoff: `env_export`

## Guardrails
- Treat `results/finish/heatmap.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/heatmap.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `env_export` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/heatmap.done` exists and `env_export` can proceed without re-running heatmap.
