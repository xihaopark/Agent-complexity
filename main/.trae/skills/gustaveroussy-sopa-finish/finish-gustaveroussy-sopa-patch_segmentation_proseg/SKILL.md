---
name: finish-gustaveroussy-sopa-patch_segmentation_proseg
description: Use this skill when orchestrating the retained "patch_segmentation_proseg" step of the gustaveroussy sopa finish finish workflow. It keeps the patch segmentation proseg stage tied to upstream `resolve_baysor` and the downstream handoff to `patch_segmentation_stardist`. It tracks completion via `results/finish/patch_segmentation_proseg.done`.
metadata:
  workflow_id: gustaveroussy-sopa-finish
  workflow_name: gustaveroussy sopa finish
  step_id: patch_segmentation_proseg
  step_name: patch segmentation proseg
---

# Scope
Use this skill only for the `patch_segmentation_proseg` step in `gustaveroussy-sopa-finish`.

## Orchestration
- Upstream requirements: `resolve_baysor`
- Step file: `finish/gustaveroussy-sopa-finish/steps/patch_segmentation_proseg.smk`
- Config file: `finish/gustaveroussy-sopa-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/patch_segmentation_proseg.done`
- Representative outputs: `results/finish/patch_segmentation_proseg.done`
- Execution targets: `patch_segmentation_proseg`
- Downstream handoff: `patch_segmentation_stardist`

## Guardrails
- Treat `results/finish/patch_segmentation_proseg.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/patch_segmentation_proseg.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `patch_segmentation_stardist` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/patch_segmentation_proseg.done` exists and `patch_segmentation_stardist` can proceed without re-running patch segmentation proseg.
