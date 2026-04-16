---
name: finish-joncahn-epigeneticbutton-plotting_mapping_stats
description: Use this skill when orchestrating the retained "plotting_mapping_stats" step of the joncahn epigeneticbutton finish finish workflow. It keeps the plotting mapping stats stage tied to upstream `prepping_mapping_stats` and the downstream handoff to `prepping_chip_peak_stats`. It tracks completion via `results/finish/plotting_mapping_stats.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: plotting_mapping_stats
  step_name: plotting mapping stats
---

# Scope
Use this skill only for the `plotting_mapping_stats` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `prepping_mapping_stats`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/plotting_mapping_stats.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plotting_mapping_stats.done`
- Representative outputs: `results/finish/plotting_mapping_stats.done`
- Execution targets: `plotting_mapping_stats`
- Downstream handoff: `prepping_chip_peak_stats`

## Guardrails
- Treat `results/finish/plotting_mapping_stats.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plotting_mapping_stats.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `prepping_chip_peak_stats` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plotting_mapping_stats.done` exists and `prepping_chip_peak_stats` can proceed without re-running plotting mapping stats.
