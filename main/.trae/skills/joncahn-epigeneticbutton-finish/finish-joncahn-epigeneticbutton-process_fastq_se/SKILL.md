---
name: finish-joncahn-epigeneticbutton-process_fastq_se
description: Use this skill when orchestrating the retained "process_fastq_se" step of the joncahn epigeneticbutton finish finish workflow. It keeps the process fastq se stage tied to upstream `process_fastq_pe` and the downstream handoff to `get_available_bam`. It tracks completion via `results/finish/process_fastq_se.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: process_fastq_se
  step_name: process fastq se
---

# Scope
Use this skill only for the `process_fastq_se` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `process_fastq_pe`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/process_fastq_se.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/process_fastq_se.done`
- Representative outputs: `results/finish/process_fastq_se.done`
- Execution targets: `process_fastq_se`
- Downstream handoff: `get_available_bam`

## Guardrails
- Treat `results/finish/process_fastq_se.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/process_fastq_se.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `get_available_bam` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/process_fastq_se.done` exists and `get_available_bam` can proceed without re-running process fastq se.
