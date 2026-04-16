---
name: finish-gustaveroussy-sopa-resolve_cellpose
description: Use this skill when orchestrating the retained "resolve_cellpose" step of the gustaveroussy sopa finish finish workflow. It keeps the resolve cellpose stage tied to upstream `patch_segmentation_cellpose` and the downstream handoff to `patch_segmentation_comseg`. It tracks completion via `results/finish/resolve_cellpose.done`.
metadata:
  workflow_id: gustaveroussy-sopa-finish
  workflow_name: gustaveroussy sopa finish
  step_id: resolve_cellpose
  step_name: resolve cellpose
---

# Scope
Use this skill only for the `resolve_cellpose` step in `gustaveroussy-sopa-finish`.

## Orchestration
- Upstream requirements: `patch_segmentation_cellpose`
- Step file: `finish/gustaveroussy-sopa-finish/steps/resolve_cellpose.smk`
- Config file: `finish/gustaveroussy-sopa-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/resolve_cellpose.done`
- Representative outputs: `results/finish/resolve_cellpose.done`
- Execution targets: `resolve_cellpose`
- Downstream handoff: `patch_segmentation_comseg`

## Guardrails
- Treat `results/finish/resolve_cellpose.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/resolve_cellpose.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `patch_segmentation_comseg` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/resolve_cellpose.done` exists and `patch_segmentation_comseg` can proceed without re-running resolve cellpose.
