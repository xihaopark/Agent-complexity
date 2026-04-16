---
name: finish-maxplanck-ie-snakepipes-get_nearest_transcript
description: Use this skill when orchestrating the retained "get_nearest_transcript" step of the maxplanck ie snakepipes finish finish workflow. It keeps the get nearest transcript stage tied to upstream `CSAW_report` and the downstream handoff to `get_nearest_gene`. It tracks completion via `results/finish/get_nearest_transcript.done`.
metadata:
  workflow_id: maxplanck-ie-snakepipes-finish
  workflow_name: maxplanck ie snakepipes finish
  step_id: get_nearest_transcript
  step_name: get nearest transcript
---

# Scope
Use this skill only for the `get_nearest_transcript` step in `maxplanck-ie-snakepipes-finish`.

## Orchestration
- Upstream requirements: `CSAW_report`
- Step file: `finish/maxplanck-ie-snakepipes-finish/steps/get_nearest_transcript.smk`
- Config file: `finish/maxplanck-ie-snakepipes-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_nearest_transcript.done`
- Representative outputs: `results/finish/get_nearest_transcript.done`
- Execution targets: `get_nearest_transcript`
- Downstream handoff: `get_nearest_gene`

## Guardrails
- Treat `results/finish/get_nearest_transcript.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_nearest_transcript.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `get_nearest_gene` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_nearest_transcript.done` exists and `get_nearest_gene` can proceed without re-running get nearest transcript.
