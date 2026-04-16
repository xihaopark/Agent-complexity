---
name: finish-joncahn-epigeneticbutton-plotting_srna_sizes_stats
description: Use this skill when orchestrating the retained "plotting_srna_sizes_stats" step of the joncahn epigeneticbutton finish finish workflow. It keeps the plotting srna sizes stats stage tied to upstream `prepping_srna_sizes_stats` and the downstream handoff to `combine_clusterfiles`. It tracks completion via `results/finish/plotting_srna_sizes_stats.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: plotting_srna_sizes_stats
  step_name: plotting srna sizes stats
---

# Scope
Use this skill only for the `plotting_srna_sizes_stats` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `prepping_srna_sizes_stats`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/plotting_srna_sizes_stats.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plotting_srna_sizes_stats.done`
- Representative outputs: `results/finish/plotting_srna_sizes_stats.done`
- Execution targets: `plotting_srna_sizes_stats`
- Downstream handoff: `combine_clusterfiles`

## Guardrails
- Treat `results/finish/plotting_srna_sizes_stats.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plotting_srna_sizes_stats.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `combine_clusterfiles` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plotting_srna_sizes_stats.done` exists and `combine_clusterfiles` can proceed without re-running plotting srna sizes stats.
