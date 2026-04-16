---
name: finish-snakemake-workflows-chipseq-sm_report_peaks_count_plot
description: Use this skill when orchestrating the retained "sm_report_peaks_count_plot" step of the snakemake workflows chipseq finish finish workflow. It keeps the sm report peaks count plot stage tied to upstream `peaks_count` and the downstream handoff to `bedtools_intersect`. It tracks completion via `results/finish/sm_report_peaks_count_plot.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: sm_report_peaks_count_plot
  step_name: sm report peaks count plot
---

# Scope
Use this skill only for the `sm_report_peaks_count_plot` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `peaks_count`
- Step file: `finish/chipseq-finish/steps/sm_report_peaks_count_plot.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/sm_report_peaks_count_plot.done`
- Representative outputs: `results/finish/sm_report_peaks_count_plot.done`
- Execution targets: `sm_report_peaks_count_plot`
- Downstream handoff: `bedtools_intersect`

## Guardrails
- Treat `results/finish/sm_report_peaks_count_plot.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/sm_report_peaks_count_plot.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `bedtools_intersect` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/sm_report_peaks_count_plot.done` exists and `bedtools_intersect` can proceed without re-running sm report peaks count plot.
