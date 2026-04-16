---
name: finish-gustaveroussy-sopa-aggregate
description: Use this skill when orchestrating the retained "aggregate" step of the gustaveroussy sopa finish finish workflow. It keeps the aggregate stage tied to upstream `patchify_transcripts` and the downstream handoff to `annotate`. It tracks completion via `results/finish/aggregate.done`.
metadata:
  workflow_id: gustaveroussy-sopa-finish
  workflow_name: gustaveroussy sopa finish
  step_id: aggregate
  step_name: aggregate
---

# Scope
Use this skill only for the `aggregate` step in `gustaveroussy-sopa-finish`.

## Orchestration
- Upstream requirements: `patchify_transcripts`
- Step file: `finish/gustaveroussy-sopa-finish/steps/aggregate.smk`
- Config file: `finish/gustaveroussy-sopa-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/aggregate.done`
- Representative outputs: `results/finish/aggregate.done`
- Execution targets: `aggregate`
- Downstream handoff: `annotate`

## Guardrails
- Treat `results/finish/aggregate.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/aggregate.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `annotate` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/aggregate.done` exists and `annotate` can proceed without re-running aggregate.
