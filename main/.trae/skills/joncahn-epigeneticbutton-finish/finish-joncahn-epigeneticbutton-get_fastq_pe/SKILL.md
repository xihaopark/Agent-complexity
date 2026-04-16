---
name: finish-joncahn-epigeneticbutton-get_fastq_pe
description: Use this skill when orchestrating the retained "get_fastq_pe" step of the joncahn epigeneticbutton finish finish workflow. It keeps the get fastq pe stage tied to upstream `check_te_file` and the downstream handoff to `get_fastq_se`. It tracks completion via `results/finish/get_fastq_pe.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: get_fastq_pe
  step_name: get fastq pe
---

# Scope
Use this skill only for the `get_fastq_pe` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `check_te_file`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/get_fastq_pe.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_fastq_pe.done`
- Representative outputs: `results/finish/get_fastq_pe.done`
- Execution targets: `get_fastq_pe`
- Downstream handoff: `get_fastq_se`

## Guardrails
- Treat `results/finish/get_fastq_pe.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_fastq_pe.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `get_fastq_se` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_fastq_pe.done` exists and `get_fastq_se` can proceed without re-running get fastq pe.
