---
name: finish-tgirke-systempiperdata-varseq-fix_tag
description: Use this skill when orchestrating the retained "fix_tag" step of the tgirke systempiperdata varseq finish finish workflow. It keeps the fix tag stage tied to upstream `mark_dup` and the downstream handoff to `hap_caller`. It tracks completion via `results/finish/fix_tag.done`.
metadata:
  workflow_id: tgirke-systempiperdata-varseq-finish
  workflow_name: tgirke systempiperdata varseq finish
  step_id: fix_tag
  step_name: fix tag
---

# Scope
Use this skill only for the `fix_tag` step in `tgirke-systempiperdata-varseq-finish`.

## Orchestration
- Upstream requirements: `mark_dup`
- Step file: `finish/tgirke-systempiperdata-varseq-finish/steps/fix_tag.smk`
- Config file: `finish/tgirke-systempiperdata-varseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/fix_tag.done`
- Representative outputs: `results/finish/fix_tag.done`
- Execution targets: `fix_tag`
- Downstream handoff: `hap_caller`

## Guardrails
- Treat `results/finish/fix_tag.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/fix_tag.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `hap_caller` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/fix_tag.done` exists and `hap_caller` can proceed without re-running fix tag.
