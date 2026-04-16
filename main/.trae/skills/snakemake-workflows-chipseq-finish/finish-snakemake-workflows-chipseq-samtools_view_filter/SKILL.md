---
name: finish-snakemake-workflows-chipseq-samtools_view_filter
description: Use this skill when orchestrating the retained "samtools_view_filter" step of the snakemake workflows chipseq finish finish workflow. It keeps the samtools view filter stage tied to upstream `mark_merged_duplicates` and the downstream handoff to `bamtools_filter_json`. It tracks completion via `results/finish/samtools_view_filter.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: samtools_view_filter
  step_name: samtools view filter
---

# Scope
Use this skill only for the `samtools_view_filter` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `mark_merged_duplicates`
- Step file: `finish/chipseq-finish/steps/samtools_view_filter.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/samtools_view_filter.done`
- Representative outputs: `results/finish/samtools_view_filter.done`
- Execution targets: `samtools_view_filter`
- Downstream handoff: `bamtools_filter_json`

## Guardrails
- Treat `results/finish/samtools_view_filter.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/samtools_view_filter.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `bamtools_filter_json` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/samtools_view_filter.done` exists and `bamtools_filter_json` can proceed without re-running samtools view filter.
