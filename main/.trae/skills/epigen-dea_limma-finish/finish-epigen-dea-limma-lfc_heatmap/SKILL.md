---
name: finish-epigen-dea-limma-lfc_heatmap
description: Use this skill when orchestrating the retained "lfc_heatmap" step of the epigen dea_limma finish finish workflow. It keeps the lfc heatmap stage tied to upstream `volcanos` and the downstream handoff to `env_export`. It tracks completion via `results/finish/lfc_heatmap.done`.
metadata:
  workflow_id: epigen-dea_limma-finish
  workflow_name: epigen dea_limma finish
  step_id: lfc_heatmap
  step_name: lfc heatmap
---

# Scope
Use this skill only for the `lfc_heatmap` step in `epigen-dea_limma-finish`.

## Orchestration
- Upstream requirements: `volcanos`
- Step file: `finish/epigen-dea_limma-finish/steps/lfc_heatmap.smk`
- Config file: `finish/epigen-dea_limma-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/lfc_heatmap.done`
- Representative outputs: `results/finish/lfc_heatmap.done`
- Execution targets: `lfc_heatmap`
- Downstream handoff: `env_export`

## Guardrails
- Treat `results/finish/lfc_heatmap.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/lfc_heatmap.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `env_export` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/lfc_heatmap.done` exists and `env_export` can proceed without re-running lfc heatmap.
