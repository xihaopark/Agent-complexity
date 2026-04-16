---
name: finish-semenko-serpent-methylation-pipeline-mark_nonconverted
description: Use this skill when orchestrating the retained "mark_nonconverted" step of the semenko serpent methylation pipeline finish finish workflow. It keeps the mark nonconverted stage tied to upstream `bwa_meth` and the downstream handoff to `samtools_fixmate_sort_markdup`. It tracks completion via `results/finish/mark_nonconverted.done`.
metadata:
  workflow_id: semenko-serpent-methylation-pipeline-finish
  workflow_name: semenko serpent methylation pipeline finish
  step_id: mark_nonconverted
  step_name: mark nonconverted
---

# Scope
Use this skill only for the `mark_nonconverted` step in `semenko-serpent-methylation-pipeline-finish`.

## Orchestration
- Upstream requirements: `bwa_meth`
- Step file: `finish/semenko-serpent-methylation-pipeline-finish/steps/mark_nonconverted.smk`
- Config file: `finish/semenko-serpent-methylation-pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/mark_nonconverted.done`
- Representative outputs: `results/finish/mark_nonconverted.done`
- Execution targets: `mark_nonconverted`
- Downstream handoff: `samtools_fixmate_sort_markdup`

## Guardrails
- Treat `results/finish/mark_nonconverted.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/mark_nonconverted.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `samtools_fixmate_sort_markdup` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/mark_nonconverted.done` exists and `samtools_fixmate_sort_markdup` can proceed without re-running mark nonconverted.
