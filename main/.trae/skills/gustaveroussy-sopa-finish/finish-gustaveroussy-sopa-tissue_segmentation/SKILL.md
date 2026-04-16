---
name: finish-gustaveroussy-sopa-tissue_segmentation
description: Use this skill when orchestrating the retained "tissue_segmentation" step of the gustaveroussy sopa finish finish workflow. It keeps the tissue segmentation stage tied to upstream `to_spatialdata` and the downstream handoff to `patchify_image`. It tracks completion via `results/finish/tissue_segmentation.done`.
metadata:
  workflow_id: gustaveroussy-sopa-finish
  workflow_name: gustaveroussy sopa finish
  step_id: tissue_segmentation
  step_name: tissue segmentation
---

# Scope
Use this skill only for the `tissue_segmentation` step in `gustaveroussy-sopa-finish`.

## Orchestration
- Upstream requirements: `to_spatialdata`
- Step file: `finish/gustaveroussy-sopa-finish/steps/tissue_segmentation.smk`
- Config file: `finish/gustaveroussy-sopa-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/tissue_segmentation.done`
- Representative outputs: `results/finish/tissue_segmentation.done`
- Execution targets: `tissue_segmentation`
- Downstream handoff: `patchify_image`

## Guardrails
- Treat `results/finish/tissue_segmentation.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/tissue_segmentation.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `patchify_image` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/tissue_segmentation.done` exists and `patchify_image` can proceed without re-running tissue segmentation.
