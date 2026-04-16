---
name: finish-snakemake-workflows-chipseq-plot_profile
description: Use this skill when orchestrating the retained "plot_profile" step of the snakemake workflows chipseq finish finish workflow. It keeps the plot profile stage tied to upstream `compute_matrix` and the downstream handoff to `plot_heatmap`. It tracks completion via `results/finish/plot_profile.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: plot_profile
  step_name: plot profile
---

# Scope
Use this skill only for the `plot_profile` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `compute_matrix`
- Step file: `finish/chipseq-finish/steps/plot_profile.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plot_profile.done`
- Representative outputs: `results/finish/plot_profile.done`
- Execution targets: `plot_profile`
- Downstream handoff: `plot_heatmap`

## Guardrails
- Treat `results/finish/plot_profile.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plot_profile.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plot_heatmap` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plot_profile.done` exists and `plot_heatmap` can proceed without re-running plot profile.
