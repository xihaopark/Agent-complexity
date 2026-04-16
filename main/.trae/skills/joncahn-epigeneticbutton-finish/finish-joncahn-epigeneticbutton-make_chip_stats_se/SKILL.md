---
name: finish-joncahn-epigeneticbutton-make_chip_stats_se
description: Use this skill when orchestrating the retained "make_chip_stats_se" step of the joncahn epigeneticbutton finish finish workflow. It keeps the make chip stats se stage tied to upstream `make_chip_stats_pe` and the downstream handoff to `pe_or_se_chip_dispatch`. It tracks completion via `results/finish/make_chip_stats_se.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: make_chip_stats_se
  step_name: make chip stats se
---

# Scope
Use this skill only for the `make_chip_stats_se` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `make_chip_stats_pe`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/make_chip_stats_se.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/make_chip_stats_se.done`
- Representative outputs: `results/finish/make_chip_stats_se.done`
- Execution targets: `make_chip_stats_se`
- Downstream handoff: `pe_or_se_chip_dispatch`

## Guardrails
- Treat `results/finish/make_chip_stats_se.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/make_chip_stats_se.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `pe_or_se_chip_dispatch` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/make_chip_stats_se.done` exists and `pe_or_se_chip_dispatch` can proceed without re-running make chip stats se.
