---
name: finish-joncahn-epigeneticbutton-download_modkit
description: Use this skill when orchestrating the retained "download_modkit" step of the joncahn epigeneticbutton finish finish workflow. It keeps the download modkit stage tied to upstream `all_mc` and the downstream handoff to `get_dmc_input`. It tracks completion via `results/finish/download_modkit.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: download_modkit
  step_name: download modkit
---

# Scope
Use this skill only for the `download_modkit` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `all_mc`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/download_modkit.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/download_modkit.done`
- Representative outputs: `results/finish/download_modkit.done`
- Execution targets: `download_modkit`
- Downstream handoff: `get_dmc_input`

## Guardrails
- Treat `results/finish/download_modkit.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/download_modkit.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `get_dmc_input` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/download_modkit.done` exists and `get_dmc_input` can proceed without re-running download modkit.
