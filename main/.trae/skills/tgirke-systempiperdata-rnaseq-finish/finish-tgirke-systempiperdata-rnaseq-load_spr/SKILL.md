---
name: finish-tgirke-systempiperdata-rnaseq-load_spr
description: Use this skill when orchestrating the retained "load_SPR" step of the tgirke systempiperdata rnaseq finish finish workflow. It keeps the load SPR stage and the downstream handoff to `preprocessing`. It tracks completion via `results/finish/load_SPR.done`.
metadata:
  workflow_id: tgirke-systempiperdata-rnaseq-finish
  workflow_name: tgirke systempiperdata rnaseq finish
  step_id: load_SPR
  step_name: load SPR
---

# Scope
Use this skill only for the `load_SPR` step in `tgirke-systempiperdata-rnaseq-finish`.

## Orchestration
- Upstream requirements: none
- Step file: `finish/tgirke-systempiperdata-rnaseq-finish/steps/load_SPR.smk`
- Config file: `finish/tgirke-systempiperdata-rnaseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/load_SPR.done`
- Representative outputs: `results/finish/load_SPR.done`
- Execution targets: `load_SPR`
- Downstream handoff: `preprocessing`

## Guardrails
- Treat `results/finish/load_SPR.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/load_SPR.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `preprocessing` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/load_SPR.done` exists and `preprocessing` can proceed without re-running load SPR.
