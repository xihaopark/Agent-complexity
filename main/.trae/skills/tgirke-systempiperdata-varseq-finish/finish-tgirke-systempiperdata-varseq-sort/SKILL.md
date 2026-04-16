---
name: finish-tgirke-systempiperdata-varseq-sort
description: Use this skill when orchestrating the retained "sort" step of the tgirke systempiperdata varseq finish finish workflow. It keeps the sort stage tied to upstream `merge_bam` and the downstream handoff to `mark_dup`. It tracks completion via `results/finish/sort.done`.
metadata:
  workflow_id: tgirke-systempiperdata-varseq-finish
  workflow_name: tgirke systempiperdata varseq finish
  step_id: sort
  step_name: sort
---

# Scope
Use this skill only for the `sort` step in `tgirke-systempiperdata-varseq-finish`.

## Orchestration
- Upstream requirements: `merge_bam`
- Step file: `finish/tgirke-systempiperdata-varseq-finish/steps/sort.smk`
- Config file: `finish/tgirke-systempiperdata-varseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/sort.done`
- Representative outputs: `results/finish/sort.done`
- Execution targets: `sort`
- Downstream handoff: `mark_dup`

## Guardrails
- Treat `results/finish/sort.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/sort.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `mark_dup` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/sort.done` exists and `mark_dup` can proceed without re-running sort.
