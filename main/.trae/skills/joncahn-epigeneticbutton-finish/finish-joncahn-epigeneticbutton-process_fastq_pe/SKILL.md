---
name: finish-joncahn-epigeneticbutton-process_fastq_pe
description: Use this skill when orchestrating the retained "process_fastq_pe" step of the joncahn epigeneticbutton finish finish workflow. It keeps the process fastq pe stage tied to upstream `run_fastqc` and the downstream handoff to `process_fastq_se`. It tracks completion via `results/finish/process_fastq_pe.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: process_fastq_pe
  step_name: process fastq pe
---

# Scope
Use this skill only for the `process_fastq_pe` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `run_fastqc`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/process_fastq_pe.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/process_fastq_pe.done`
- Representative outputs: `results/finish/process_fastq_pe.done`
- Execution targets: `process_fastq_pe`
- Downstream handoff: `process_fastq_se`

## Guardrails
- Treat `results/finish/process_fastq_pe.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/process_fastq_pe.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `process_fastq_se` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/process_fastq_pe.done` exists and `process_fastq_se` can proceed without re-running process fastq pe.
