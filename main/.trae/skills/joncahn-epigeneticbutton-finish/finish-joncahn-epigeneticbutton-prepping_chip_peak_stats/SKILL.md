---
name: finish-joncahn-epigeneticbutton-prepping_chip_peak_stats
description: Use this skill when orchestrating the retained "prepping_chip_peak_stats" step of the joncahn epigeneticbutton finish finish workflow. It keeps the prepping chip peak stats stage tied to upstream `plotting_mapping_stats` and the downstream handoff to `plotting_peaks_stats_chip_tf`. It tracks completion via `results/finish/prepping_chip_peak_stats.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: prepping_chip_peak_stats
  step_name: prepping chip peak stats
---

# Scope
Use this skill only for the `prepping_chip_peak_stats` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `plotting_mapping_stats`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/prepping_chip_peak_stats.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/prepping_chip_peak_stats.done`
- Representative outputs: `results/finish/prepping_chip_peak_stats.done`
- Execution targets: `prepping_chip_peak_stats`
- Downstream handoff: `plotting_peaks_stats_chip_tf`

## Guardrails
- Treat `results/finish/prepping_chip_peak_stats.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/prepping_chip_peak_stats.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plotting_peaks_stats_chip_tf` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/prepping_chip_peak_stats.done` exists and `plotting_peaks_stats_chip_tf` can proceed without re-running prepping chip peak stats.
