---
name: finish-semenko-serpent-methylation-pipeline-multiqc
description: Use this skill when orchestrating the retained "multiqc" step of the semenko serpent methylation pipeline finish finish workflow. It keeps the multiqc stage tied to upstream `touch_complete_flag` and the downstream handoff to `all`. It tracks completion via `results/finish/multiqc.done`.
metadata:
  workflow_id: semenko-serpent-methylation-pipeline-finish
  workflow_name: semenko serpent methylation pipeline finish
  step_id: multiqc
  step_name: multiqc
---

# Scope
Use this skill only for the `multiqc` step in `semenko-serpent-methylation-pipeline-finish`.

## Orchestration
- Upstream requirements: `touch_complete_flag`
- Step file: `finish/semenko-serpent-methylation-pipeline-finish/steps/multiqc.smk`
- Config file: `finish/semenko-serpent-methylation-pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/multiqc.done`
- Representative outputs: `results/finish/multiqc.done`
- Execution targets: `multiqc`
- Downstream handoff: `all`

## Guardrails
- Treat `results/finish/multiqc.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/multiqc.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `all` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/multiqc.done` exists and `all` can proceed without re-running multiqc.
