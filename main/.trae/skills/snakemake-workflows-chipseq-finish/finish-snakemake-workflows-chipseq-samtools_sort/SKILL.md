---
name: finish-snakemake-workflows-chipseq-samtools_sort
description: Use this skill when orchestrating the retained "samtools_sort" step of the snakemake workflows chipseq finish finish workflow. It keeps the samtools sort stage tied to upstream `bamtools_filter_json` and the downstream handoff to `orphan_remove`. It tracks completion via `results/finish/samtools_sort.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: samtools_sort
  step_name: samtools sort
---

# Scope
Use this skill only for the `samtools_sort` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `bamtools_filter_json`
- Step file: `finish/chipseq-finish/steps/samtools_sort.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/samtools_sort.done`
- Representative outputs: `results/finish/samtools_sort.done`
- Execution targets: `samtools_sort`
- Downstream handoff: `orphan_remove`

## Guardrails
- Treat `results/finish/samtools_sort.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/samtools_sort.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `orphan_remove` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/samtools_sort.done` exists and `orphan_remove` can proceed without re-running samtools sort.
