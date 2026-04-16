---
name: finish-joncahn-epigeneticbutton-check_gff
description: Use this skill when orchestrating the retained "check_gff" step of the joncahn epigeneticbutton finish finish workflow. It keeps the check gff stage tied to upstream `check_fasta` and the downstream handoff to `check_gtf`. It tracks completion via `results/finish/check_gff.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: check_gff
  step_name: check gff
---

# Scope
Use this skill only for the `check_gff` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `check_fasta`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/check_gff.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/check_gff.done`
- Representative outputs: `results/finish/check_gff.done`
- Execution targets: `check_gff`
- Downstream handoff: `check_gtf`

## Guardrails
- Treat `results/finish/check_gff.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/check_gff.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `check_gtf` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/check_gff.done` exists and `check_gtf` can proceed without re-running check gff.
