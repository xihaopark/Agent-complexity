---
name: finish-joncahn-epigeneticbutton-prepare_reference
description: Use this skill when orchestrating the retained "prepare_reference" step of the joncahn epigeneticbutton finish finish workflow. It keeps the prepare reference stage tied to upstream `combined_analysis` and the downstream handoff to `check_fasta`. It tracks completion via `results/finish/prepare_reference.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: prepare_reference
  step_name: prepare reference
---

# Scope
Use this skill only for the `prepare_reference` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `combined_analysis`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/prepare_reference.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/prepare_reference.done`
- Representative outputs: `results/finish/prepare_reference.done`
- Execution targets: `prepare_reference`
- Downstream handoff: `check_fasta`

## Guardrails
- Treat `results/finish/prepare_reference.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/prepare_reference.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `check_fasta` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/prepare_reference.done` exists and `check_fasta` can proceed without re-running prepare reference.
