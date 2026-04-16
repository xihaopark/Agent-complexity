---
name: finish-joncahn-epigeneticbutton-prepare_modbam_for_pileup
description: Use this skill when orchestrating the retained "prepare_modbam_for_pileup" step of the joncahn epigeneticbutton finish finish workflow. It keeps the prepare modbam for pileup stage tied to upstream `dmc_input_checkpoint` and the downstream handoff to `modkit_pileup_dmc`. It tracks completion via `results/finish/prepare_modbam_for_pileup.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: prepare_modbam_for_pileup
  step_name: prepare modbam for pileup
---

# Scope
Use this skill only for the `prepare_modbam_for_pileup` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `dmc_input_checkpoint`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/prepare_modbam_for_pileup.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/prepare_modbam_for_pileup.done`
- Representative outputs: `results/finish/prepare_modbam_for_pileup.done`
- Execution targets: `prepare_modbam_for_pileup`
- Downstream handoff: `modkit_pileup_dmc`

## Guardrails
- Treat `results/finish/prepare_modbam_for_pileup.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/prepare_modbam_for_pileup.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `modkit_pileup_dmc` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/prepare_modbam_for_pileup.done` exists and `modkit_pileup_dmc` can proceed without re-running prepare modbam for pileup.
