---
name: finish-joncahn-epigeneticbutton-map_only
description: Use this skill when orchestrating the retained "map_only" step of the joncahn epigeneticbutton finish finish workflow. It keeps the map only stage and the downstream handoff to `coverage_chip`. It tracks completion via `results/finish/map_only.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: map_only
  step_name: map only
---

# Scope
Use this skill only for the `map_only` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: none
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/map_only.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/map_only.done`
- Representative outputs: `results/finish/map_only.done`
- Execution targets: `map_only`
- Downstream handoff: `coverage_chip`

## Guardrails
- Treat `results/finish/map_only.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/map_only.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `coverage_chip` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/map_only.done` exists and `coverage_chip` can proceed without re-running map only.
