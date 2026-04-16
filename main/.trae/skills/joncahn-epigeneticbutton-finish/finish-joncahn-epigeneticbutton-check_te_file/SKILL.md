---
name: finish-joncahn-epigeneticbutton-check_te_file
description: Use this skill when orchestrating the retained "check_te_file" step of the joncahn epigeneticbutton finish finish workflow. It keeps the check te file stage tied to upstream `prep_region_file` and the downstream handoff to `get_fastq_pe`. It tracks completion via `results/finish/check_te_file.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: check_te_file
  step_name: check te file
---

# Scope
Use this skill only for the `check_te_file` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `prep_region_file`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/check_te_file.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/check_te_file.done`
- Representative outputs: `results/finish/check_te_file.done`
- Execution targets: `check_te_file`
- Downstream handoff: `get_fastq_pe`

## Guardrails
- Treat `results/finish/check_te_file.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/check_te_file.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `get_fastq_pe` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/check_te_file.done` exists and `get_fastq_pe` can proceed without re-running check te file.
