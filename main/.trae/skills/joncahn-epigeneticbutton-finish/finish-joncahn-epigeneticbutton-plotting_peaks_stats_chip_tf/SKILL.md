---
name: finish-joncahn-epigeneticbutton-plotting_peaks_stats_chip_tf
description: Use this skill when orchestrating the retained "plotting_peaks_stats_chip_tf" step of the joncahn epigeneticbutton finish finish workflow. It keeps the plotting peaks stats chip tf stage tied to upstream `prepping_chip_peak_stats` and the downstream handoff to `prepping_srna_sizes_stats`. It tracks completion via `results/finish/plotting_peaks_stats_chip_tf.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: plotting_peaks_stats_chip_tf
  step_name: plotting peaks stats chip tf
---

# Scope
Use this skill only for the `plotting_peaks_stats_chip_tf` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `prepping_chip_peak_stats`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/plotting_peaks_stats_chip_tf.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plotting_peaks_stats_chip_tf.done`
- Representative outputs: `results/finish/plotting_peaks_stats_chip_tf.done`
- Execution targets: `plotting_peaks_stats_chip_tf`
- Downstream handoff: `prepping_srna_sizes_stats`

## Guardrails
- Treat `results/finish/plotting_peaks_stats_chip_tf.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plotting_peaks_stats_chip_tf.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `prepping_srna_sizes_stats` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plotting_peaks_stats_chip_tf.done` exists and `prepping_srna_sizes_stats` can proceed without re-running plotting peaks stats chip tf.
