---
name: finish-tgirke-systempiperdata-varseq-mark_dup
description: Use this skill when orchestrating the retained "mark_dup" step of the tgirke systempiperdata varseq finish finish workflow. It keeps the mark dup stage tied to upstream `sort` and the downstream handoff to `fix_tag`. It tracks completion via `results/finish/mark_dup.done`.
metadata:
  workflow_id: tgirke-systempiperdata-varseq-finish
  workflow_name: tgirke systempiperdata varseq finish
  step_id: mark_dup
  step_name: mark dup
---

# Scope
Use this skill only for the `mark_dup` step in `tgirke-systempiperdata-varseq-finish`.

## Orchestration
- Upstream requirements: `sort`
- Step file: `finish/tgirke-systempiperdata-varseq-finish/steps/mark_dup.smk`
- Config file: `finish/tgirke-systempiperdata-varseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/mark_dup.done`
- Representative outputs: `results/finish/mark_dup.done`
- Execution targets: `mark_dup`
- Downstream handoff: `fix_tag`

## Guardrails
- Treat `results/finish/mark_dup.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/mark_dup.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `fix_tag` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/mark_dup.done` exists and `fix_tag` can proceed without re-running mark dup.
