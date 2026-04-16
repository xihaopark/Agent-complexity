---
name: finish-tgirke-systempiperdata-varseq-hap_caller
description: Use this skill when orchestrating the retained "hap_caller" step of the tgirke systempiperdata varseq finish finish workflow. It keeps the hap caller stage tied to upstream `fix_tag` and the downstream handoff to `import`. It tracks completion via `results/finish/hap_caller.done`.
metadata:
  workflow_id: tgirke-systempiperdata-varseq-finish
  workflow_name: tgirke systempiperdata varseq finish
  step_id: hap_caller
  step_name: hap caller
---

# Scope
Use this skill only for the `hap_caller` step in `tgirke-systempiperdata-varseq-finish`.

## Orchestration
- Upstream requirements: `fix_tag`
- Step file: `finish/tgirke-systempiperdata-varseq-finish/steps/hap_caller.smk`
- Config file: `finish/tgirke-systempiperdata-varseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/hap_caller.done`
- Representative outputs: `results/finish/hap_caller.done`
- Execution targets: `hap_caller`
- Downstream handoff: `import`

## Guardrails
- Treat `results/finish/hap_caller.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/hap_caller.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `import` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/hap_caller.done` exists and `import` can proceed without re-running hap caller.
