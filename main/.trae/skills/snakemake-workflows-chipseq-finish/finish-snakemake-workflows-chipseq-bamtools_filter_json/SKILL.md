---
name: finish-snakemake-workflows-chipseq-bamtools_filter_json
description: Use this skill when orchestrating the retained "bamtools_filter_json" step of the snakemake workflows chipseq finish finish workflow. It keeps the bamtools filter json stage tied to upstream `samtools_view_filter` and the downstream handoff to `samtools_sort`. It tracks completion via `results/finish/bamtools_filter_json.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: bamtools_filter_json
  step_name: bamtools filter json
---

# Scope
Use this skill only for the `bamtools_filter_json` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `samtools_view_filter`
- Step file: `finish/chipseq-finish/steps/bamtools_filter_json.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/bamtools_filter_json.done`
- Representative outputs: `results/finish/bamtools_filter_json.done`
- Execution targets: `bamtools_filter_json`
- Downstream handoff: `samtools_sort`

## Guardrails
- Treat `results/finish/bamtools_filter_json.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/bamtools_filter_json.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `samtools_sort` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/bamtools_filter_json.done` exists and `samtools_sort` can proceed without re-running bamtools filter json.
