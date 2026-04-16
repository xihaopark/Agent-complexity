---
name: finish-snakemake-workflows-chipseq-plot_homer_annotatepeaks
description: Use this skill when orchestrating the retained "plot_homer_annotatepeaks" step of the snakemake workflows chipseq finish finish workflow. It keeps the plot homer annotatepeaks stage tied to upstream `plot_macs_qc` and the downstream handoff to `plot_sum_annotatepeaks`. It tracks completion via `results/finish/plot_homer_annotatepeaks.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: plot_homer_annotatepeaks
  step_name: plot homer annotatepeaks
---

# Scope
Use this skill only for the `plot_homer_annotatepeaks` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `plot_macs_qc`
- Step file: `finish/chipseq-finish/steps/plot_homer_annotatepeaks.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plot_homer_annotatepeaks.done`
- Representative outputs: `results/finish/plot_homer_annotatepeaks.done`
- Execution targets: `plot_homer_annotatepeaks`
- Downstream handoff: `plot_sum_annotatepeaks`

## Guardrails
- Treat `results/finish/plot_homer_annotatepeaks.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plot_homer_annotatepeaks.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plot_sum_annotatepeaks` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plot_homer_annotatepeaks.done` exists and `plot_sum_annotatepeaks` can proceed without re-running plot homer annotatepeaks.
