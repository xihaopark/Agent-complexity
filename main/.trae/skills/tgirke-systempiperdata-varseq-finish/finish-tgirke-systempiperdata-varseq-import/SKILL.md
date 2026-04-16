---
name: finish-tgirke-systempiperdata-varseq-import
description: Use this skill when orchestrating the retained "import" step of the tgirke systempiperdata varseq finish finish workflow. It keeps the import stage tied to upstream `hap_caller` and the downstream handoff to `call_variants`. It tracks completion via `results/finish/import.done`.
metadata:
  workflow_id: tgirke-systempiperdata-varseq-finish
  workflow_name: tgirke systempiperdata varseq finish
  step_id: import
  step_name: import
---

# Scope
Use this skill only for the `import` step in `tgirke-systempiperdata-varseq-finish`.

## Orchestration
- Upstream requirements: `hap_caller`
- Step file: `finish/tgirke-systempiperdata-varseq-finish/steps/import.smk`
- Config file: `finish/tgirke-systempiperdata-varseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/import.done`
- Representative outputs: `results/finish/import.done`
- Execution targets: `import`
- Downstream handoff: `call_variants`

## Guardrails
- Treat `results/finish/import.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/import.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `call_variants` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/import.done` exists and `call_variants` can proceed without re-running import.
