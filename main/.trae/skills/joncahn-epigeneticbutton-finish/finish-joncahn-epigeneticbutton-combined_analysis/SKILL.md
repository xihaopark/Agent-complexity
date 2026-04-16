---
name: finish-joncahn-epigeneticbutton-combined_analysis
description: Use this skill when orchestrating the retained "combined_analysis" step of the joncahn epigeneticbutton finish finish workflow. It keeps the combined analysis stage tied to upstream `coverage_chip` and the downstream handoff to `prepare_reference`. It tracks completion via `results/finish/combined_analysis.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: combined_analysis
  step_name: combined analysis
---

# Scope
Use this skill only for the `combined_analysis` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `coverage_chip`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/combined_analysis.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/combined_analysis.done`
- Representative outputs: `results/finish/combined_analysis.done`
- Execution targets: `combined_analysis`
- Downstream handoff: `prepare_reference`

## Guardrails
- Treat `results/finish/combined_analysis.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/combined_analysis.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `prepare_reference` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/combined_analysis.done` exists and `prepare_reference` can proceed without re-running combined analysis.
