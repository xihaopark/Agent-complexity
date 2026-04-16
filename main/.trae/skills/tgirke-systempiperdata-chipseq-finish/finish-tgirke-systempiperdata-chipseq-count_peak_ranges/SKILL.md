---
name: finish-tgirke-systempiperdata-chipseq-count_peak_ranges
description: Use this skill when orchestrating the retained "count_peak_ranges" step of the tgirke systempiperdata chipseq finish finish workflow. It keeps the count peak ranges stage tied to upstream `annotation_ChIPpeakAnno` and the downstream handoff to `diff_bind_analysis`. It tracks completion via `results/finish/count_peak_ranges.done`.
metadata:
  workflow_id: tgirke-systempiperdata-chipseq-finish
  workflow_name: tgirke systempiperdata chipseq finish
  step_id: count_peak_ranges
  step_name: count peak ranges
---

# Scope
Use this skill only for the `count_peak_ranges` step in `tgirke-systempiperdata-chipseq-finish`.

## Orchestration
- Upstream requirements: `annotation_ChIPpeakAnno`
- Step file: `finish/tgirke-systempiperdata-chipseq-finish/steps/count_peak_ranges.smk`
- Config file: `finish/tgirke-systempiperdata-chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/count_peak_ranges.done`
- Representative outputs: `results/finish/count_peak_ranges.done`
- Execution targets: `count_peak_ranges`
- Downstream handoff: `diff_bind_analysis`

## Guardrails
- Treat `results/finish/count_peak_ranges.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/count_peak_ranges.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `diff_bind_analysis` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/count_peak_ranges.done` exists and `diff_bind_analysis` can proceed without re-running count peak ranges.
