---
name: finish-semenko-serpent-methylation-pipeline-fastqc_bam
description: Use this skill when orchestrating the retained "fastqc_bam" step of the semenko serpent methylation pipeline finish finish workflow. It keeps the fastqc bam stage tied to upstream `methyldackel_mbias_plots` and the downstream handoff to `goleft_indexcov`. It tracks completion via `results/finish/fastqc_bam.done`.
metadata:
  workflow_id: semenko-serpent-methylation-pipeline-finish
  workflow_name: semenko serpent methylation pipeline finish
  step_id: fastqc_bam
  step_name: fastqc bam
---

# Scope
Use this skill only for the `fastqc_bam` step in `semenko-serpent-methylation-pipeline-finish`.

## Orchestration
- Upstream requirements: `methyldackel_mbias_plots`
- Step file: `finish/semenko-serpent-methylation-pipeline-finish/steps/fastqc_bam.smk`
- Config file: `finish/semenko-serpent-methylation-pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/fastqc_bam.done`
- Representative outputs: `results/finish/fastqc_bam.done`
- Execution targets: `fastqc_bam`
- Downstream handoff: `goleft_indexcov`

## Guardrails
- Treat `results/finish/fastqc_bam.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/fastqc_bam.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `goleft_indexcov` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/fastqc_bam.done` exists and `goleft_indexcov` can proceed without re-running fastqc bam.
