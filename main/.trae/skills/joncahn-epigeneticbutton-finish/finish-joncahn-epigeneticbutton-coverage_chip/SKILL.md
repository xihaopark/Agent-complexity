---
name: finish-joncahn-epigeneticbutton-coverage_chip
description: Use this skill when orchestrating the retained "coverage_chip" step of the joncahn epigeneticbutton finish finish workflow. It keeps the coverage chip stage tied to upstream `map_only` and the downstream handoff to `combined_analysis`. It tracks completion via `results/finish/coverage_chip.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: coverage_chip
  step_name: coverage chip
---

# Scope
Use this skill only for the `coverage_chip` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `map_only`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/coverage_chip.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/coverage_chip.done`
- Representative outputs: `results/finish/coverage_chip.done`
- Execution targets: `coverage_chip`
- Downstream handoff: `combined_analysis`

## Guardrails
- Treat `results/finish/coverage_chip.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/coverage_chip.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `combined_analysis` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/coverage_chip.done` exists and `combined_analysis` can proceed without re-running coverage chip.
