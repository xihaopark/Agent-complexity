---
name: finish-gustaveroussy-sopa-annotate
description: Use this skill when orchestrating the retained "annotate" step of the gustaveroussy sopa finish finish workflow. It keeps the annotate stage tied to upstream `aggregate` and the downstream handoff to `scanpy_preprocess`. It tracks completion via `results/finish/annotate.done`.
metadata:
  workflow_id: gustaveroussy-sopa-finish
  workflow_name: gustaveroussy sopa finish
  step_id: annotate
  step_name: annotate
---

# Scope
Use this skill only for the `annotate` step in `gustaveroussy-sopa-finish`.

## Orchestration
- Upstream requirements: `aggregate`
- Step file: `finish/gustaveroussy-sopa-finish/steps/annotate.smk`
- Config file: `finish/gustaveroussy-sopa-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/annotate.done`
- Representative outputs: `results/finish/annotate.done`
- Execution targets: `annotate`
- Downstream handoff: `scanpy_preprocess`

## Guardrails
- Treat `results/finish/annotate.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/annotate.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `scanpy_preprocess` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/annotate.done` exists and `scanpy_preprocess` can proceed without re-running annotate.
