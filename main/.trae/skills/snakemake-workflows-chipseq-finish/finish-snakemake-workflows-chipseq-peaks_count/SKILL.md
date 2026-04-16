---
name: finish-snakemake-workflows-chipseq-peaks_count
description: Use this skill when orchestrating the retained "peaks_count" step of the snakemake workflows chipseq finish finish workflow. It keeps the peaks count stage tied to upstream `macs2_callpeak_narrow` and the downstream handoff to `sm_report_peaks_count_plot`. It tracks completion via `results/finish/peaks_count.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: peaks_count
  step_name: peaks count
---

# Scope
Use this skill only for the `peaks_count` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `macs2_callpeak_narrow`
- Step file: `finish/chipseq-finish/steps/peaks_count.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/peaks_count.done`
- Representative outputs: `results/finish/peaks_count.done`
- Execution targets: `peaks_count`
- Downstream handoff: `sm_report_peaks_count_plot`

## Guardrails
- Treat `results/finish/peaks_count.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/peaks_count.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `sm_report_peaks_count_plot` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/peaks_count.done` exists and `sm_report_peaks_count_plot` can proceed without re-running peaks count.
