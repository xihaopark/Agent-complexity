---
name: finish-epigen-fetch-ngs-merge_metadata
description: Use this skill when orchestrating the retained "merge_metadata" step of the epigen fetch_ngs finish finish workflow. It keeps the merge metadata stage tied to upstream `fetch_file` and the downstream handoff to `all`. It tracks completion via `results/finish/merge_metadata.done`.
metadata:
  workflow_id: epigen-fetch_ngs-finish
  workflow_name: epigen fetch_ngs finish
  step_id: merge_metadata
  step_name: merge metadata
---

# Scope
Use this skill only for the `merge_metadata` step in `epigen-fetch_ngs-finish`.

## Orchestration
- Upstream requirements: `fetch_file`
- Step file: `finish/epigen-fetch_ngs-finish/steps/merge_metadata.smk`
- Config file: `finish/epigen-fetch_ngs-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/merge_metadata.done`
- Representative outputs: `results/finish/merge_metadata.done`
- Execution targets: `merge_metadata`
- Downstream handoff: `all`

## Guardrails
- Treat `results/finish/merge_metadata.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/merge_metadata.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `all` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/merge_metadata.done` exists and `all` can proceed without re-running merge metadata.
