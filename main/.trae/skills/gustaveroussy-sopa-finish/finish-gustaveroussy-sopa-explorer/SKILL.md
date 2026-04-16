---
name: finish-gustaveroussy-sopa-explorer
description: Use this skill when orchestrating the retained "explorer" step of the gustaveroussy sopa finish finish workflow. It keeps the explorer stage tied to upstream `explorer_raw` and the downstream handoff to `report`. It tracks completion via `results/finish/explorer.done`.
metadata:
  workflow_id: gustaveroussy-sopa-finish
  workflow_name: gustaveroussy sopa finish
  step_id: explorer
  step_name: explorer
---

# Scope
Use this skill only for the `explorer` step in `gustaveroussy-sopa-finish`.

## Orchestration
- Upstream requirements: `explorer_raw`
- Step file: `finish/gustaveroussy-sopa-finish/steps/explorer.smk`
- Config file: `finish/gustaveroussy-sopa-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/explorer.done`
- Representative outputs: `results/finish/explorer.done`
- Execution targets: `explorer`
- Downstream handoff: `report`

## Guardrails
- Treat `results/finish/explorer.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/explorer.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `report` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/explorer.done` exists and `report` can proceed without re-running explorer.
