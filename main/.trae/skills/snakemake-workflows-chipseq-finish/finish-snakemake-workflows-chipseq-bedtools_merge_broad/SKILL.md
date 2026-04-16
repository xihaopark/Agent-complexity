---
name: finish-snakemake-workflows-chipseq-bedtools_merge_broad
description: Use this skill when orchestrating the retained "bedtools_merge_broad" step of the snakemake workflows chipseq finish finish workflow. It keeps the bedtools merge broad stage tied to upstream `plot_sum_annotatepeaks` and the downstream handoff to `bedtools_merge_narrow`. It tracks completion via `results/finish/bedtools_merge_broad.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: bedtools_merge_broad
  step_name: bedtools merge broad
---

# Scope
Use this skill only for the `bedtools_merge_broad` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `plot_sum_annotatepeaks`
- Step file: `finish/chipseq-finish/steps/bedtools_merge_broad.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/bedtools_merge_broad.done`
- Representative outputs: `results/finish/bedtools_merge_broad.done`
- Execution targets: `bedtools_merge_broad`
- Downstream handoff: `bedtools_merge_narrow`

## Guardrails
- Treat `results/finish/bedtools_merge_broad.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/bedtools_merge_broad.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `bedtools_merge_narrow` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/bedtools_merge_broad.done` exists and `bedtools_merge_narrow` can proceed without re-running bedtools merge broad.
