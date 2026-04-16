---
name: finish-semenko-serpent-methylation-pipeline-samtools_statistics
description: Use this skill when orchestrating the retained "samtools_statistics" step of the semenko serpent methylation pipeline finish finish workflow. It keeps the samtools statistics stage tied to upstream `samtools_index` and the downstream handoff to `biscuit_bed`. It tracks completion via `results/finish/samtools_statistics.done`.
metadata:
  workflow_id: semenko-serpent-methylation-pipeline-finish
  workflow_name: semenko serpent methylation pipeline finish
  step_id: samtools_statistics
  step_name: samtools statistics
---

# Scope
Use this skill only for the `samtools_statistics` step in `semenko-serpent-methylation-pipeline-finish`.

## Orchestration
- Upstream requirements: `samtools_index`
- Step file: `finish/semenko-serpent-methylation-pipeline-finish/steps/samtools_statistics.smk`
- Config file: `finish/semenko-serpent-methylation-pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/samtools_statistics.done`
- Representative outputs: `results/finish/samtools_statistics.done`
- Execution targets: `samtools_statistics`
- Downstream handoff: `biscuit_bed`

## Guardrails
- Treat `results/finish/samtools_statistics.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/samtools_statistics.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `biscuit_bed` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/samtools_statistics.done` exists and `biscuit_bed` can proceed without re-running samtools statistics.
