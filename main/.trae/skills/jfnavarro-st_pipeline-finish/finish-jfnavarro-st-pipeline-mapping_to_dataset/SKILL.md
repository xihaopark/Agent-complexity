---
name: finish-jfnavarro-st-pipeline-mapping_to_dataset
description: Use this skill when orchestrating the retained "mapping_to_dataset" step of the jfnavarro st_pipeline finish finish workflow. It keeps the Mapping To Dataset stage tied to upstream `filtering`. It tracks completion via `results/finish/mapping_to_dataset.done`.
metadata:
  workflow_id: jfnavarro-st_pipeline-finish
  workflow_name: jfnavarro st_pipeline finish
  step_id: mapping_to_dataset
  step_name: Mapping To Dataset
---

# Scope
Use this skill only for the `mapping_to_dataset` step in `jfnavarro-st_pipeline-finish`.

## Orchestration
- Upstream requirements: `filtering`
- Step file: `finish/jfnavarro-st_pipeline-finish/steps/mapping_to_dataset.smk`
- Config file: `finish/jfnavarro-st_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/mapping_to_dataset.done`
- Representative outputs: `results/finish/mapping_to_dataset.done`
- Execution targets: `mapping_to_dataset`
- Downstream handoff: none

## Guardrails
- Treat `results/finish/mapping_to_dataset.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/mapping_to_dataset.smk` so the step remains separable and replayable inside the finish workflow.

## Done Criteria
Mark this step complete only when `results/finish/mapping_to_dataset.done` exists and matches the intended step boundary.
