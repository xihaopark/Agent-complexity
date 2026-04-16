---
name: finish-semenko-serpent-methylation-pipeline-biscuit_qc
description: Use this skill when orchestrating the retained "biscuit_qc" step of the semenko serpent methylation pipeline finish finish workflow. It keeps the biscuit qc stage tied to upstream `biscuit_epiread` and the downstream handoff to `methyldackel_mbias_plots`. It tracks completion via `results/finish/biscuit_qc.done`.
metadata:
  workflow_id: semenko-serpent-methylation-pipeline-finish
  workflow_name: semenko serpent methylation pipeline finish
  step_id: biscuit_qc
  step_name: biscuit qc
---

# Scope
Use this skill only for the `biscuit_qc` step in `semenko-serpent-methylation-pipeline-finish`.

## Orchestration
- Upstream requirements: `biscuit_epiread`
- Step file: `finish/semenko-serpent-methylation-pipeline-finish/steps/biscuit_qc.smk`
- Config file: `finish/semenko-serpent-methylation-pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/biscuit_qc.done`
- Representative outputs: `results/finish/biscuit_qc.done`
- Execution targets: `biscuit_qc`
- Downstream handoff: `methyldackel_mbias_plots`

## Guardrails
- Treat `results/finish/biscuit_qc.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/biscuit_qc.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `methyldackel_mbias_plots` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/biscuit_qc.done` exists and `methyldackel_mbias_plots` can proceed without re-running biscuit qc.
