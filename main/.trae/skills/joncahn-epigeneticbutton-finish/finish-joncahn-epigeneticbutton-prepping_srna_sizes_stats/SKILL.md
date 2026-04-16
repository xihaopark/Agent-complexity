---
name: finish-joncahn-epigeneticbutton-prepping_srna_sizes_stats
description: Use this skill when orchestrating the retained "prepping_srna_sizes_stats" step of the joncahn epigeneticbutton finish finish workflow. It keeps the prepping srna sizes stats stage tied to upstream `plotting_peaks_stats_chip_tf` and the downstream handoff to `plotting_srna_sizes_stats`. It tracks completion via `results/finish/prepping_srna_sizes_stats.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: prepping_srna_sizes_stats
  step_name: prepping srna sizes stats
---

# Scope
Use this skill only for the `prepping_srna_sizes_stats` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `plotting_peaks_stats_chip_tf`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/prepping_srna_sizes_stats.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/prepping_srna_sizes_stats.done`
- Representative outputs: `results/finish/prepping_srna_sizes_stats.done`
- Execution targets: `prepping_srna_sizes_stats`
- Downstream handoff: `plotting_srna_sizes_stats`

## Guardrails
- Treat `results/finish/prepping_srna_sizes_stats.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/prepping_srna_sizes_stats.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plotting_srna_sizes_stats` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/prepping_srna_sizes_stats.done` exists and `plotting_srna_sizes_stats` can proceed without re-running prepping srna sizes stats.
