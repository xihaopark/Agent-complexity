---
name: finish-epigen-dea-seurat-aggregate
description: Use this skill when orchestrating the retained "aggregate" step of the epigen dea_seurat finish finish workflow. It keeps the aggregate stage tied to upstream `dea` and the downstream handoff to `feature_lists`. It tracks completion via `results/finish/aggregate.done`.
metadata:
  workflow_id: epigen-dea_seurat-finish
  workflow_name: epigen dea_seurat finish
  step_id: aggregate
  step_name: aggregate
---

# Scope
Use this skill only for the `aggregate` step in `epigen-dea_seurat-finish`.

## Orchestration
- Upstream requirements: `dea`
- Step file: `finish/epigen-dea_seurat-finish/steps/aggregate.smk`
- Config file: `finish/epigen-dea_seurat-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/aggregate.done`
- Representative outputs: `results/finish/aggregate.done`
- Execution targets: `aggregate`
- Downstream handoff: `feature_lists`

## Guardrails
- Treat `results/finish/aggregate.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/aggregate.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `feature_lists` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/aggregate.done` exists and `feature_lists` can proceed without re-running aggregate.
