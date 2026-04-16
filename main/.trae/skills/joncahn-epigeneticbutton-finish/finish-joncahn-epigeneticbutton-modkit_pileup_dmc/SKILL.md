---
name: finish-joncahn-epigeneticbutton-modkit_pileup_dmc
description: Use this skill when orchestrating the retained "modkit_pileup_dmc" step of the joncahn epigeneticbutton finish finish workflow. It keeps the modkit pileup dmc stage tied to upstream `prepare_modbam_for_pileup` and the downstream handoff to `copy_bedmethyl_input`. It tracks completion via `results/finish/modkit_pileup_dmc.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: modkit_pileup_dmc
  step_name: modkit pileup dmc
---

# Scope
Use this skill only for the `modkit_pileup_dmc` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `prepare_modbam_for_pileup`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/modkit_pileup_dmc.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/modkit_pileup_dmc.done`
- Representative outputs: `results/finish/modkit_pileup_dmc.done`
- Execution targets: `modkit_pileup_dmc`
- Downstream handoff: `copy_bedmethyl_input`

## Guardrails
- Treat `results/finish/modkit_pileup_dmc.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/modkit_pileup_dmc.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `copy_bedmethyl_input` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/modkit_pileup_dmc.done` exists and `copy_bedmethyl_input` can proceed without re-running modkit pileup dmc.
