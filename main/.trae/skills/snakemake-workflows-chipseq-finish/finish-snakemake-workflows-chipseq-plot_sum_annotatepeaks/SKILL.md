---
name: finish-snakemake-workflows-chipseq-plot_sum_annotatepeaks
description: Use this skill when orchestrating the retained "plot_sum_annotatepeaks" step of the snakemake workflows chipseq finish finish workflow. It keeps the plot sum annotatepeaks stage tied to upstream `plot_homer_annotatepeaks` and the downstream handoff to `bedtools_merge_broad`. It tracks completion via `results/finish/plot_sum_annotatepeaks.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: plot_sum_annotatepeaks
  step_name: plot sum annotatepeaks
---

# Scope
Use this skill only for the `plot_sum_annotatepeaks` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `plot_homer_annotatepeaks`
- Step file: `finish/chipseq-finish/steps/plot_sum_annotatepeaks.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plot_sum_annotatepeaks.done`
- Representative outputs: `results/finish/plot_sum_annotatepeaks.done`
- Execution targets: `plot_sum_annotatepeaks`
- Downstream handoff: `bedtools_merge_broad`

## Guardrails
- Treat `results/finish/plot_sum_annotatepeaks.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plot_sum_annotatepeaks.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `bedtools_merge_broad` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plot_sum_annotatepeaks.done` exists and `bedtools_merge_broad` can proceed without re-running plot sum annotatepeaks.
