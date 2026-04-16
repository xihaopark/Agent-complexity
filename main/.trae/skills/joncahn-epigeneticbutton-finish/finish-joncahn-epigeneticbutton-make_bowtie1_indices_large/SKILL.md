---
name: finish-joncahn-epigeneticbutton-make_bowtie1_indices_large
description: Use this skill when orchestrating the retained "make_bowtie1_indices_large" step of the joncahn epigeneticbutton finish finish workflow. It keeps the make bowtie1 indices large stage tied to upstream `make_bowtie1_indices` and the downstream handoff to `shortstack_map`. It tracks completion via `results/finish/make_bowtie1_indices_large.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: make_bowtie1_indices_large
  step_name: make bowtie1 indices large
---

# Scope
Use this skill only for the `make_bowtie1_indices_large` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `make_bowtie1_indices`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/make_bowtie1_indices_large.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/make_bowtie1_indices_large.done`
- Representative outputs: `results/finish/make_bowtie1_indices_large.done`
- Execution targets: `make_bowtie1_indices_large`
- Downstream handoff: `shortstack_map`

## Guardrails
- Treat `results/finish/make_bowtie1_indices_large.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/make_bowtie1_indices_large.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `shortstack_map` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/make_bowtie1_indices_large.done` exists and `shortstack_map` can proceed without re-running make bowtie1 indices large.
