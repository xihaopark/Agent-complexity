---
name: finish-gustaveroussy-sopa-patch_segmentation_stardist
description: Use this skill when orchestrating the retained "patch_segmentation_stardist" step of the gustaveroussy sopa finish finish workflow. It keeps the patch segmentation stardist stage tied to upstream `patch_segmentation_proseg` and the downstream handoff to `resolve_stardist`. It tracks completion via `results/finish/patch_segmentation_stardist.done`.
metadata:
  workflow_id: gustaveroussy-sopa-finish
  workflow_name: gustaveroussy sopa finish
  step_id: patch_segmentation_stardist
  step_name: patch segmentation stardist
---

# Scope
Use this skill only for the `patch_segmentation_stardist` step in `gustaveroussy-sopa-finish`.

## Orchestration
- Upstream requirements: `patch_segmentation_proseg`
- Step file: `finish/gustaveroussy-sopa-finish/steps/patch_segmentation_stardist.smk`
- Config file: `finish/gustaveroussy-sopa-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/patch_segmentation_stardist.done`
- Representative outputs: `results/finish/patch_segmentation_stardist.done`
- Execution targets: `patch_segmentation_stardist`
- Downstream handoff: `resolve_stardist`

## Guardrails
- Treat `results/finish/patch_segmentation_stardist.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/patch_segmentation_stardist.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `resolve_stardist` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/patch_segmentation_stardist.done` exists and `resolve_stardist` can proceed without re-running patch segmentation stardist.
