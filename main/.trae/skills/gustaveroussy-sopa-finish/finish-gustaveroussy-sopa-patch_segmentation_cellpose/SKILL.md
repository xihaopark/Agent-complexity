---
name: finish-gustaveroussy-sopa-patch_segmentation_cellpose
description: Use this skill when orchestrating the retained "patch_segmentation_cellpose" step of the gustaveroussy sopa finish finish workflow. It keeps the patch segmentation cellpose stage tied to upstream `report` and the downstream handoff to `resolve_cellpose`. It tracks completion via `results/finish/patch_segmentation_cellpose.done`.
metadata:
  workflow_id: gustaveroussy-sopa-finish
  workflow_name: gustaveroussy sopa finish
  step_id: patch_segmentation_cellpose
  step_name: patch segmentation cellpose
---

# Scope
Use this skill only for the `patch_segmentation_cellpose` step in `gustaveroussy-sopa-finish`.

## Orchestration
- Upstream requirements: `report`
- Step file: `finish/gustaveroussy-sopa-finish/steps/patch_segmentation_cellpose.smk`
- Config file: `finish/gustaveroussy-sopa-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/patch_segmentation_cellpose.done`
- Representative outputs: `results/finish/patch_segmentation_cellpose.done`
- Execution targets: `patch_segmentation_cellpose`
- Downstream handoff: `resolve_cellpose`

## Guardrails
- Treat `results/finish/patch_segmentation_cellpose.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/patch_segmentation_cellpose.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `resolve_cellpose` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/patch_segmentation_cellpose.done` exists and `resolve_cellpose` can proceed without re-running patch segmentation cellpose.
