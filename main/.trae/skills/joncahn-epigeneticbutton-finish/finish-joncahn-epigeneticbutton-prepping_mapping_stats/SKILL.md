---
name: finish-joncahn-epigeneticbutton-prepping_mapping_stats
description: Use this skill when orchestrating the retained "prepping_mapping_stats" step of the joncahn epigeneticbutton finish finish workflow. It keeps the prepping mapping stats stage tied to upstream `is_stranded` and the downstream handoff to `plotting_mapping_stats`. It tracks completion via `results/finish/prepping_mapping_stats.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: prepping_mapping_stats
  step_name: prepping mapping stats
---

# Scope
Use this skill only for the `prepping_mapping_stats` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `is_stranded`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/prepping_mapping_stats.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/prepping_mapping_stats.done`
- Representative outputs: `results/finish/prepping_mapping_stats.done`
- Execution targets: `prepping_mapping_stats`
- Downstream handoff: `plotting_mapping_stats`

## Guardrails
- Treat `results/finish/prepping_mapping_stats.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/prepping_mapping_stats.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plotting_mapping_stats` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/prepping_mapping_stats.done` exists and `plotting_mapping_stats` can proceed without re-running prepping mapping stats.
