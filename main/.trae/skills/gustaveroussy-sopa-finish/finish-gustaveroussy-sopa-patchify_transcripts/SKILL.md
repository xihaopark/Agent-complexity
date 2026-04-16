---
name: finish-gustaveroussy-sopa-patchify_transcripts
description: Use this skill when orchestrating the retained "patchify_transcripts" step of the gustaveroussy sopa finish finish workflow. It keeps the patchify transcripts stage tied to upstream `patchify_image` and the downstream handoff to `aggregate`. It tracks completion via `results/finish/patchify_transcripts.done`.
metadata:
  workflow_id: gustaveroussy-sopa-finish
  workflow_name: gustaveroussy sopa finish
  step_id: patchify_transcripts
  step_name: patchify transcripts
---

# Scope
Use this skill only for the `patchify_transcripts` step in `gustaveroussy-sopa-finish`.

## Orchestration
- Upstream requirements: `patchify_image`
- Step file: `finish/gustaveroussy-sopa-finish/steps/patchify_transcripts.smk`
- Config file: `finish/gustaveroussy-sopa-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/patchify_transcripts.done`
- Representative outputs: `results/finish/patchify_transcripts.done`
- Execution targets: `patchify_transcripts`
- Downstream handoff: `aggregate`

## Guardrails
- Treat `results/finish/patchify_transcripts.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/patchify_transcripts.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `aggregate` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/patchify_transcripts.done` exists and `aggregate` can proceed without re-running patchify transcripts.
