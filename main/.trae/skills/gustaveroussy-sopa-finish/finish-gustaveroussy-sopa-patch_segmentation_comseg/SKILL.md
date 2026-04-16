---
name: finish-gustaveroussy-sopa-patch_segmentation_comseg
description: Use this skill when orchestrating the retained "patch_segmentation_comseg" step of the gustaveroussy sopa finish finish workflow. It keeps the patch segmentation comseg stage tied to upstream `resolve_cellpose` and the downstream handoff to `resolve_comseg`. It tracks completion via `results/finish/patch_segmentation_comseg.done`.
metadata:
  workflow_id: gustaveroussy-sopa-finish
  workflow_name: gustaveroussy sopa finish
  step_id: patch_segmentation_comseg
  step_name: patch segmentation comseg
---

# Scope
Use this skill only for the `patch_segmentation_comseg` step in `gustaveroussy-sopa-finish`.

## Orchestration
- Upstream requirements: `resolve_cellpose`
- Step file: `finish/gustaveroussy-sopa-finish/steps/patch_segmentation_comseg.smk`
- Config file: `finish/gustaveroussy-sopa-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/patch_segmentation_comseg.done`
- Representative outputs: `results/finish/patch_segmentation_comseg.done`
- Execution targets: `patch_segmentation_comseg`
- Downstream handoff: `resolve_comseg`

## Guardrails
- Treat `results/finish/patch_segmentation_comseg.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/patch_segmentation_comseg.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `resolve_comseg` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/patch_segmentation_comseg.done` exists and `resolve_comseg` can proceed without re-running patch segmentation comseg.
