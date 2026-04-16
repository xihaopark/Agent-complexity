---
name: finish-joncahn-epigeneticbutton-run_fastqc
description: Use this skill when orchestrating the retained "run_fastqc" step of the joncahn epigeneticbutton finish finish workflow. It keeps the run fastqc stage tied to upstream `get_fastq_se` and the downstream handoff to `process_fastq_pe`. It tracks completion via `results/finish/run_fastqc.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: run_fastqc
  step_name: run fastqc
---

# Scope
Use this skill only for the `run_fastqc` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `get_fastq_se`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/run_fastqc.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/run_fastqc.done`
- Representative outputs: `results/finish/run_fastqc.done`
- Execution targets: `run_fastqc`
- Downstream handoff: `process_fastq_pe`

## Guardrails
- Treat `results/finish/run_fastqc.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/run_fastqc.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `process_fastq_pe` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/run_fastqc.done` exists and `process_fastq_pe` can proceed without re-running run fastqc.
