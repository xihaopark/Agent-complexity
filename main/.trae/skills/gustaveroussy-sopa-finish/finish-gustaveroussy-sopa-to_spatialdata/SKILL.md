---
name: finish-gustaveroussy-sopa-to_spatialdata
description: Use this skill when orchestrating the retained "to_spatialdata" step of the gustaveroussy sopa finish finish workflow. It keeps the to spatialdata stage and the downstream handoff to `tissue_segmentation`. It tracks completion via `results/finish/to_spatialdata.done`.
metadata:
  workflow_id: gustaveroussy-sopa-finish
  workflow_name: gustaveroussy sopa finish
  step_id: to_spatialdata
  step_name: to spatialdata
---

# Scope
Use this skill only for the `to_spatialdata` step in `gustaveroussy-sopa-finish`.

## Orchestration
- Upstream requirements: none
- Step file: `finish/gustaveroussy-sopa-finish/steps/to_spatialdata.smk`
- Config file: `finish/gustaveroussy-sopa-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/to_spatialdata.done`
- Representative outputs: `results/finish/to_spatialdata.done`
- Execution targets: `to_spatialdata`
- Downstream handoff: `tissue_segmentation`

## Guardrails
- Treat `results/finish/to_spatialdata.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/to_spatialdata.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `tissue_segmentation` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/to_spatialdata.done` exists and `tissue_segmentation` can proceed without re-running to spatialdata.
