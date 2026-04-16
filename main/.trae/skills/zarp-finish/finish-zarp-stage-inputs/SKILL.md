---
name: finish-zarp-stage-inputs
description: Use this skill when orchestrating the retained "stage_inputs" step of the Zarp finish workflow. It stages reads and metadata after configuration validation and prepares the workflow for trimming.
metadata:
  workflow_id: zarp-finish
  workflow_name: Zarp Finish Workflow
  step_id: stage_inputs
  step_name: Stage input reads and metadata
---

# Scope
Use this skill only for the `stage_inputs` step in `zarp-finish`.

## Orchestration
- Upstream requirements: `validate_config`
- Step file: `finish/zarp-finish/steps/stage_inputs.smk`
- Config file: `finish/zarp-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/stage_inputs.done`
- Representative outputs: `output/staged_inputs/*`
- Downstream handoff: `trimming`

## Guardrails
- Treat `results/finish/stage_inputs.done` as the authoritative completion signal for this wrapped finish step.
- Keep this step focused on staging input assets and metadata, not on trimming or alignment.

## Done Criteria
Mark this step complete only when staged reads and metadata are materialized and the trimming step can use them directly.
