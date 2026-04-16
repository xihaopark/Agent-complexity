---
name: finish-gustaveroussy-sopa-scanpy_preprocess
description: Use this skill when orchestrating the retained "scanpy_preprocess" step of the gustaveroussy sopa finish finish workflow. It keeps the scanpy preprocess stage tied to upstream `annotate` and the downstream handoff to `explorer_raw`. It tracks completion via `results/finish/scanpy_preprocess.done`.
metadata:
  workflow_id: gustaveroussy-sopa-finish
  workflow_name: gustaveroussy sopa finish
  step_id: scanpy_preprocess
  step_name: scanpy preprocess
---

# Scope
Use this skill only for the `scanpy_preprocess` step in `gustaveroussy-sopa-finish`.

## Orchestration
- Upstream requirements: `annotate`
- Step file: `finish/gustaveroussy-sopa-finish/steps/scanpy_preprocess.smk`
- Config file: `finish/gustaveroussy-sopa-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/scanpy_preprocess.done`
- Representative outputs: `results/finish/scanpy_preprocess.done`
- Execution targets: `scanpy_preprocess`
- Downstream handoff: `explorer_raw`

## Guardrails
- Treat `results/finish/scanpy_preprocess.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/scanpy_preprocess.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `explorer_raw` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/scanpy_preprocess.done` exists and `explorer_raw` can proceed without re-running scanpy preprocess.
