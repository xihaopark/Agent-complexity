---
name: finish-joncahn-epigeneticbutton-get_fastq_se
description: Use this skill when orchestrating the retained "get_fastq_se" step of the joncahn epigeneticbutton finish finish workflow. It keeps the get fastq se stage tied to upstream `get_fastq_pe` and the downstream handoff to `run_fastqc`. It tracks completion via `results/finish/get_fastq_se.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: get_fastq_se
  step_name: get fastq se
---

# Scope
Use this skill only for the `get_fastq_se` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `get_fastq_pe`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/get_fastq_se.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_fastq_se.done`
- Representative outputs: `results/finish/get_fastq_se.done`
- Execution targets: `get_fastq_se`
- Downstream handoff: `run_fastqc`

## Guardrails
- Treat `results/finish/get_fastq_se.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_fastq_se.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `run_fastqc` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_fastq_se.done` exists and `run_fastqc` can proceed without re-running get fastq se.
