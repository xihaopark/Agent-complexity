---
name: finish-joncahn-epigeneticbutton-filter_chip_se
description: Use this skill when orchestrating the retained "filter_chip_se" step of the joncahn epigeneticbutton finish finish workflow. It keeps the filter chip se stage tied to upstream `filter_chip_pe` and the downstream handoff to `make_chip_stats_pe`. It tracks completion via `results/finish/filter_chip_se.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: filter_chip_se
  step_name: filter chip se
---

# Scope
Use this skill only for the `filter_chip_se` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `filter_chip_pe`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/filter_chip_se.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/filter_chip_se.done`
- Representative outputs: `results/finish/filter_chip_se.done`
- Execution targets: `filter_chip_se`
- Downstream handoff: `make_chip_stats_pe`

## Guardrails
- Treat `results/finish/filter_chip_se.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/filter_chip_se.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `make_chip_stats_pe` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/filter_chip_se.done` exists and `make_chip_stats_pe` can proceed without re-running filter chip se.
