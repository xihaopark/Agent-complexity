---
name: finish-gustaveroussy-sopa-resolve_stardist
description: Use this skill when orchestrating the retained "resolve_stardist" step of the gustaveroussy sopa finish finish workflow. It keeps the resolve stardist stage tied to upstream `patch_segmentation_stardist` and the downstream handoff to `all`. It tracks completion via `results/finish/resolve_stardist.done`.
metadata:
  workflow_id: gustaveroussy-sopa-finish
  workflow_name: gustaveroussy sopa finish
  step_id: resolve_stardist
  step_name: resolve stardist
---

# Scope
Use this skill only for the `resolve_stardist` step in `gustaveroussy-sopa-finish`.

## Orchestration
- Upstream requirements: `patch_segmentation_stardist`
- Step file: `finish/gustaveroussy-sopa-finish/steps/resolve_stardist.smk`
- Config file: `finish/gustaveroussy-sopa-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/resolve_stardist.done`
- Representative outputs: `results/finish/resolve_stardist.done`
- Execution targets: `resolve_stardist`
- Downstream handoff: `all`

## Guardrails
- Treat `results/finish/resolve_stardist.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/resolve_stardist.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `all` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/resolve_stardist.done` exists and `all` can proceed without re-running resolve stardist.
