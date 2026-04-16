---
name: finish-gustaveroussy-sopa-patchify_image
description: Use this skill when orchestrating the retained "patchify_image" step of the gustaveroussy sopa finish finish workflow. It keeps the patchify image stage tied to upstream `tissue_segmentation` and the downstream handoff to `patchify_transcripts`. It tracks completion via `results/finish/patchify_image.done`.
metadata:
  workflow_id: gustaveroussy-sopa-finish
  workflow_name: gustaveroussy sopa finish
  step_id: patchify_image
  step_name: patchify image
---

# Scope
Use this skill only for the `patchify_image` step in `gustaveroussy-sopa-finish`.

## Orchestration
- Upstream requirements: `tissue_segmentation`
- Step file: `finish/gustaveroussy-sopa-finish/steps/patchify_image.smk`
- Config file: `finish/gustaveroussy-sopa-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/patchify_image.done`
- Representative outputs: `results/finish/patchify_image.done`
- Execution targets: `patchify_image`
- Downstream handoff: `patchify_transcripts`

## Guardrails
- Treat `results/finish/patchify_image.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/patchify_image.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `patchify_transcripts` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/patchify_image.done` exists and `patchify_transcripts` can proceed without re-running patchify image.
