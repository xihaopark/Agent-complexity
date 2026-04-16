---
name: finish-gustaveroussy-sopa-patch_segmentation_baysor
description: Use this skill when orchestrating the retained "patch_segmentation_baysor" step of the gustaveroussy sopa finish finish workflow. It keeps the patch segmentation baysor stage tied to upstream `resolve_comseg` and the downstream handoff to `resolve_baysor`. It tracks completion via `results/finish/patch_segmentation_baysor.done`.
metadata:
  workflow_id: gustaveroussy-sopa-finish
  workflow_name: gustaveroussy sopa finish
  step_id: patch_segmentation_baysor
  step_name: patch segmentation baysor
---

# Scope
Use this skill only for the `patch_segmentation_baysor` step in `gustaveroussy-sopa-finish`.

## Orchestration
- Upstream requirements: `resolve_comseg`
- Step file: `finish/gustaveroussy-sopa-finish/steps/patch_segmentation_baysor.smk`
- Config file: `finish/gustaveroussy-sopa-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/patch_segmentation_baysor.done`
- Representative outputs: `results/finish/patch_segmentation_baysor.done`
- Execution targets: `patch_segmentation_baysor`
- Downstream handoff: `resolve_baysor`

## Guardrails
- Treat `results/finish/patch_segmentation_baysor.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/patch_segmentation_baysor.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `resolve_baysor` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/patch_segmentation_baysor.done` exists and `resolve_baysor` can proceed without re-running patch segmentation baysor.
