---
name: finish-semenko-serpent-methylation-pipeline-biscuit_epiread
description: Use this skill when orchestrating the retained "biscuit_epiread" step of the semenko serpent methylation pipeline finish finish workflow. It keeps the biscuit epiread stage tied to upstream `biscuit_bed` and the downstream handoff to `biscuit_qc`. It tracks completion via `results/finish/biscuit_epiread.done`.
metadata:
  workflow_id: semenko-serpent-methylation-pipeline-finish
  workflow_name: semenko serpent methylation pipeline finish
  step_id: biscuit_epiread
  step_name: biscuit epiread
---

# Scope
Use this skill only for the `biscuit_epiread` step in `semenko-serpent-methylation-pipeline-finish`.

## Orchestration
- Upstream requirements: `biscuit_bed`
- Step file: `finish/semenko-serpent-methylation-pipeline-finish/steps/biscuit_epiread.smk`
- Config file: `finish/semenko-serpent-methylation-pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/biscuit_epiread.done`
- Representative outputs: `results/finish/biscuit_epiread.done`
- Execution targets: `biscuit_epiread`
- Downstream handoff: `biscuit_qc`

## Guardrails
- Treat `results/finish/biscuit_epiread.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/biscuit_epiread.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `biscuit_qc` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/biscuit_epiread.done` exists and `biscuit_qc` can proceed without re-running biscuit epiread.
