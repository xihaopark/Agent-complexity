---
name: finish-joncahn-epigeneticbutton-check_fasta
description: Use this skill when orchestrating the retained "check_fasta" step of the joncahn epigeneticbutton finish finish workflow. It keeps the check fasta stage tied to upstream `prepare_reference` and the downstream handoff to `check_gff`. It tracks completion via `results/finish/check_fasta.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: check_fasta
  step_name: check fasta
---

# Scope
Use this skill only for the `check_fasta` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `prepare_reference`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/check_fasta.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/check_fasta.done`
- Representative outputs: `results/finish/check_fasta.done`
- Execution targets: `check_fasta`
- Downstream handoff: `check_gff`

## Guardrails
- Treat `results/finish/check_fasta.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/check_fasta.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `check_gff` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/check_fasta.done` exists and `check_gff` can proceed without re-running check fasta.
