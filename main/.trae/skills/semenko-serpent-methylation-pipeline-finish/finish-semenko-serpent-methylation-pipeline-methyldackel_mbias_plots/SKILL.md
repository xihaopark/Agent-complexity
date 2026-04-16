---
name: finish-semenko-serpent-methylation-pipeline-methyldackel_mbias_plots
description: Use this skill when orchestrating the retained "methyldackel_mbias_plots" step of the semenko serpent methylation pipeline finish finish workflow. It keeps the methyldackel mbias plots stage tied to upstream `biscuit_qc` and the downstream handoff to `fastqc_bam`. It tracks completion via `results/finish/methyldackel_mbias_plots.done`.
metadata:
  workflow_id: semenko-serpent-methylation-pipeline-finish
  workflow_name: semenko serpent methylation pipeline finish
  step_id: methyldackel_mbias_plots
  step_name: methyldackel mbias plots
---

# Scope
Use this skill only for the `methyldackel_mbias_plots` step in `semenko-serpent-methylation-pipeline-finish`.

## Orchestration
- Upstream requirements: `biscuit_qc`
- Step file: `finish/semenko-serpent-methylation-pipeline-finish/steps/methyldackel_mbias_plots.smk`
- Config file: `finish/semenko-serpent-methylation-pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/methyldackel_mbias_plots.done`
- Representative outputs: `results/finish/methyldackel_mbias_plots.done`
- Execution targets: `methyldackel_mbias_plots`
- Downstream handoff: `fastqc_bam`

## Guardrails
- Treat `results/finish/methyldackel_mbias_plots.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/methyldackel_mbias_plots.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `fastqc_bam` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/methyldackel_mbias_plots.done` exists and `fastqc_bam` can proceed without re-running methyldackel mbias plots.
