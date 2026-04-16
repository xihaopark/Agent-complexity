---
name: finish-jfnavarro-st-pipeline-filtering
description: Use this skill when orchestrating the retained "filtering" step of the jfnavarro st_pipeline finish finish workflow. It keeps the Filtering stage and the downstream handoff to `mapping_to_dataset`. It tracks completion via `results/finish/filtering.done`.
metadata:
  workflow_id: jfnavarro-st_pipeline-finish
  workflow_name: jfnavarro st_pipeline finish
  step_id: filtering
  step_name: Filtering
---

# Scope
Use this skill only for the `filtering` step in `jfnavarro-st_pipeline-finish`.

## Orchestration
- Upstream requirements: none
- Step file: `finish/jfnavarro-st_pipeline-finish/steps/filtering.smk`
- Config file: `finish/jfnavarro-st_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/filtering.done`
- Representative outputs: `results/finish/filtering.done`
- Execution targets: `filtering`
- Downstream handoff: `mapping_to_dataset`

## Guardrails
- Treat `results/finish/filtering.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/filtering.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `mapping_to_dataset` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/filtering.done` exists and `mapping_to_dataset` can proceed without re-running Filtering.
