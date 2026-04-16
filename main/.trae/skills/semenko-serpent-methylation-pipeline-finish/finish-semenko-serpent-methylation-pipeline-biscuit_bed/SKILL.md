---
name: finish-semenko-serpent-methylation-pipeline-biscuit_bed
description: Use this skill when orchestrating the retained "biscuit_bed" step of the semenko serpent methylation pipeline finish finish workflow. It keeps the biscuit bed stage tied to upstream `samtools_statistics` and the downstream handoff to `biscuit_epiread`. It tracks completion via `results/finish/biscuit_bed.done`.
metadata:
  workflow_id: semenko-serpent-methylation-pipeline-finish
  workflow_name: semenko serpent methylation pipeline finish
  step_id: biscuit_bed
  step_name: biscuit bed
---

# Scope
Use this skill only for the `biscuit_bed` step in `semenko-serpent-methylation-pipeline-finish`.

## Orchestration
- Upstream requirements: `samtools_statistics`
- Step file: `finish/semenko-serpent-methylation-pipeline-finish/steps/biscuit_bed.smk`
- Config file: `finish/semenko-serpent-methylation-pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/biscuit_bed.done`
- Representative outputs: `results/finish/biscuit_bed.done`
- Execution targets: `biscuit_bed`
- Downstream handoff: `biscuit_epiread`

## Guardrails
- Treat `results/finish/biscuit_bed.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/biscuit_bed.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `biscuit_epiread` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/biscuit_bed.done` exists and `biscuit_epiread` can proceed without re-running biscuit bed.
