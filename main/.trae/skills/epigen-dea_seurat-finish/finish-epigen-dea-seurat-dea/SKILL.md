---
name: finish-epigen-dea-seurat-dea
description: Use this skill when orchestrating the retained "dea" step of the epigen dea_seurat finish finish workflow. It keeps the dea stage and the downstream handoff to `aggregate`. It tracks completion via `results/finish/dea.done`.
metadata:
  workflow_id: epigen-dea_seurat-finish
  workflow_name: epigen dea_seurat finish
  step_id: dea
  step_name: dea
---

# Scope
Use this skill only for the `dea` step in `epigen-dea_seurat-finish`.

## Orchestration
- Upstream requirements: none
- Step file: `finish/epigen-dea_seurat-finish/steps/dea.smk`
- Config file: `finish/epigen-dea_seurat-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/dea.done`
- Representative outputs: `results/finish/dea.done`
- Execution targets: `dea`
- Downstream handoff: `aggregate`

## Guardrails
- Treat `results/finish/dea.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/dea.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `aggregate` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/dea.done` exists and `aggregate` can proceed without re-running dea.
