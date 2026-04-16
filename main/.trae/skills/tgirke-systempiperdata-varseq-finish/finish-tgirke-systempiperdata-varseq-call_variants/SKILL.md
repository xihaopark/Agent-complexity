---
name: finish-tgirke-systempiperdata-varseq-call_variants
description: Use this skill when orchestrating the retained "call_variants" step of the tgirke systempiperdata varseq finish finish workflow. It keeps the call variants stage tied to upstream `import` and the downstream handoff to `filter`. It tracks completion via `results/finish/call_variants.done`.
metadata:
  workflow_id: tgirke-systempiperdata-varseq-finish
  workflow_name: tgirke systempiperdata varseq finish
  step_id: call_variants
  step_name: call variants
---

# Scope
Use this skill only for the `call_variants` step in `tgirke-systempiperdata-varseq-finish`.

## Orchestration
- Upstream requirements: `import`
- Step file: `finish/tgirke-systempiperdata-varseq-finish/steps/call_variants.smk`
- Config file: `finish/tgirke-systempiperdata-varseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/call_variants.done`
- Representative outputs: `results/finish/call_variants.done`
- Execution targets: `call_variants`
- Downstream handoff: `filter`

## Guardrails
- Treat `results/finish/call_variants.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/call_variants.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `filter` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/call_variants.done` exists and `filter` can proceed without re-running call variants.
