---
name: finish-joncahn-epigeneticbutton-get_dmc_input
description: Use this skill when orchestrating the retained "get_dmc_input" step of the joncahn epigeneticbutton finish finish workflow. It keeps the get dmc input stage tied to upstream `download_modkit` and the downstream handoff to `dmc_input_checkpoint`. It tracks completion via `results/finish/get_dmc_input.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: get_dmc_input
  step_name: get dmc input
---

# Scope
Use this skill only for the `get_dmc_input` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `download_modkit`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/get_dmc_input.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_dmc_input.done`
- Representative outputs: `results/finish/get_dmc_input.done`
- Execution targets: `get_dmc_input`
- Downstream handoff: `dmc_input_checkpoint`

## Guardrails
- Treat `results/finish/get_dmc_input.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_dmc_input.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `dmc_input_checkpoint` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_dmc_input.done` exists and `dmc_input_checkpoint` can proceed without re-running get dmc input.
