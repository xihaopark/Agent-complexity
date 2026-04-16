---
name: finish-joncahn-epigeneticbutton-is_stranded
description: Use this skill when orchestrating the retained "is_stranded" step of the joncahn epigeneticbutton finish finish workflow. It keeps the is stranded stage tied to upstream `has_header` and the downstream handoff to `prepping_mapping_stats`. It tracks completion via `results/finish/is_stranded.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: is_stranded
  step_name: is stranded
---

# Scope
Use this skill only for the `is_stranded` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `has_header`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/is_stranded.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/is_stranded.done`
- Representative outputs: `results/finish/is_stranded.done`
- Execution targets: `is_stranded`
- Downstream handoff: `prepping_mapping_stats`

## Guardrails
- Treat `results/finish/is_stranded.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/is_stranded.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `prepping_mapping_stats` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/is_stranded.done` exists and `prepping_mapping_stats` can proceed without re-running is stranded.
