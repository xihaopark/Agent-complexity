---
name: finish-snakemake-workflows-chipseq-bedtools_intersect
description: Use this skill when orchestrating the retained "bedtools_intersect" step of the snakemake workflows chipseq finish finish workflow. It keeps the bedtools intersect stage tied to upstream `sm_report_peaks_count_plot` and the downstream handoff to `frip_score`. It tracks completion via `results/finish/bedtools_intersect.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: bedtools_intersect
  step_name: bedtools intersect
---

# Scope
Use this skill only for the `bedtools_intersect` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `sm_report_peaks_count_plot`
- Step file: `finish/chipseq-finish/steps/bedtools_intersect.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/bedtools_intersect.done`
- Representative outputs: `results/finish/bedtools_intersect.done`
- Execution targets: `bedtools_intersect`
- Downstream handoff: `frip_score`

## Guardrails
- Treat `results/finish/bedtools_intersect.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/bedtools_intersect.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `frip_score` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/bedtools_intersect.done` exists and `frip_score` can proceed without re-running bedtools intersect.
