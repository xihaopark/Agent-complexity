---
name: finish-gustaveroussy-sopa-explorer_raw
description: Use this skill when orchestrating the retained "explorer_raw" step of the gustaveroussy sopa finish finish workflow. It keeps the explorer raw stage tied to upstream `scanpy_preprocess` and the downstream handoff to `explorer`. It tracks completion via `results/finish/explorer_raw.done`.
metadata:
  workflow_id: gustaveroussy-sopa-finish
  workflow_name: gustaveroussy sopa finish
  step_id: explorer_raw
  step_name: explorer raw
---

# Scope
Use this skill only for the `explorer_raw` step in `gustaveroussy-sopa-finish`.

## Orchestration
- Upstream requirements: `scanpy_preprocess`
- Step file: `finish/gustaveroussy-sopa-finish/steps/explorer_raw.smk`
- Config file: `finish/gustaveroussy-sopa-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/explorer_raw.done`
- Representative outputs: `results/finish/explorer_raw.done`
- Execution targets: `explorer_raw`
- Downstream handoff: `explorer`

## Guardrails
- Treat `results/finish/explorer_raw.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/explorer_raw.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `explorer` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/explorer_raw.done` exists and `explorer` can proceed without re-running explorer raw.
