---
name: finish-gustaveroussy-sopa-resolve_comseg
description: Use this skill when orchestrating the retained "resolve_comseg" step of the gustaveroussy sopa finish finish workflow. It keeps the resolve comseg stage tied to upstream `patch_segmentation_comseg` and the downstream handoff to `patch_segmentation_baysor`. It tracks completion via `results/finish/resolve_comseg.done`.
metadata:
  workflow_id: gustaveroussy-sopa-finish
  workflow_name: gustaveroussy sopa finish
  step_id: resolve_comseg
  step_name: resolve comseg
---

# Scope
Use this skill only for the `resolve_comseg` step in `gustaveroussy-sopa-finish`.

## Orchestration
- Upstream requirements: `patch_segmentation_comseg`
- Step file: `finish/gustaveroussy-sopa-finish/steps/resolve_comseg.smk`
- Config file: `finish/gustaveroussy-sopa-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/resolve_comseg.done`
- Representative outputs: `results/finish/resolve_comseg.done`
- Execution targets: `resolve_comseg`
- Downstream handoff: `patch_segmentation_baysor`

## Guardrails
- Treat `results/finish/resolve_comseg.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/resolve_comseg.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `patch_segmentation_baysor` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/resolve_comseg.done` exists and `patch_segmentation_baysor` can proceed without re-running resolve comseg.
