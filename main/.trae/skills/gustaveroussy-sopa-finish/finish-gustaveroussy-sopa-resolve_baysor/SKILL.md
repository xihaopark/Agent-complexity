---
name: finish-gustaveroussy-sopa-resolve_baysor
description: Use this skill when orchestrating the retained "resolve_baysor" step of the gustaveroussy sopa finish finish workflow. It keeps the resolve baysor stage tied to upstream `patch_segmentation_baysor` and the downstream handoff to `patch_segmentation_proseg`. It tracks completion via `results/finish/resolve_baysor.done`.
metadata:
  workflow_id: gustaveroussy-sopa-finish
  workflow_name: gustaveroussy sopa finish
  step_id: resolve_baysor
  step_name: resolve baysor
---

# Scope
Use this skill only for the `resolve_baysor` step in `gustaveroussy-sopa-finish`.

## Orchestration
- Upstream requirements: `patch_segmentation_baysor`
- Step file: `finish/gustaveroussy-sopa-finish/steps/resolve_baysor.smk`
- Config file: `finish/gustaveroussy-sopa-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/resolve_baysor.done`
- Representative outputs: `results/finish/resolve_baysor.done`
- Execution targets: `resolve_baysor`
- Downstream handoff: `patch_segmentation_proseg`

## Guardrails
- Treat `results/finish/resolve_baysor.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/resolve_baysor.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `patch_segmentation_proseg` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/resolve_baysor.done` exists and `patch_segmentation_proseg` can proceed without re-running resolve baysor.
