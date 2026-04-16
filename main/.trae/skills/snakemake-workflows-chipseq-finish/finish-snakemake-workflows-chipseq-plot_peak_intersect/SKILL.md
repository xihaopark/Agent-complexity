---
name: finish-snakemake-workflows-chipseq-plot_peak_intersect
description: Use this skill when orchestrating the retained "plot_peak_intersect" step of the snakemake workflows chipseq finish finish workflow. It keeps the plot peak intersect stage tied to upstream `create_consensus_saf` and the downstream handoff to `create_consensus_igv`. It tracks completion via `results/finish/plot_peak_intersect.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: plot_peak_intersect
  step_name: plot peak intersect
---

# Scope
Use this skill only for the `plot_peak_intersect` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `create_consensus_saf`
- Step file: `finish/chipseq-finish/steps/plot_peak_intersect.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plot_peak_intersect.done`
- Representative outputs: `results/finish/plot_peak_intersect.done`
- Execution targets: `plot_peak_intersect`
- Downstream handoff: `create_consensus_igv`

## Guardrails
- Treat `results/finish/plot_peak_intersect.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plot_peak_intersect.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `create_consensus_igv` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plot_peak_intersect.done` exists and `create_consensus_igv` can proceed without re-running plot peak intersect.
