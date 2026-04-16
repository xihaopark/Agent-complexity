---
name: finish-joncahn-epigeneticbutton-dmc_input_checkpoint
description: Use this skill when orchestrating the retained "dmc_input_checkpoint" step of the joncahn epigeneticbutton finish finish workflow. It keeps the dmc input checkpoint stage tied to upstream `get_dmc_input` and the downstream handoff to `prepare_modbam_for_pileup`. It tracks completion via `results/finish/dmc_input_checkpoint.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: dmc_input_checkpoint
  step_name: dmc input checkpoint
---

# Scope
Use this skill only for the `dmc_input_checkpoint` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `get_dmc_input`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/dmc_input_checkpoint.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/dmc_input_checkpoint.done`
- Representative outputs: `results/finish/dmc_input_checkpoint.done`
- Execution targets: `dmc_input_checkpoint`
- Downstream handoff: `prepare_modbam_for_pileup`

## Guardrails
- Treat `results/finish/dmc_input_checkpoint.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/dmc_input_checkpoint.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `prepare_modbam_for_pileup` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/dmc_input_checkpoint.done` exists and `prepare_modbam_for_pileup` can proceed without re-running dmc input checkpoint.
