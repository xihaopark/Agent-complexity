---
name: finish-tgirke-systempiperdata-varseq-load_spr
description: Use this skill when orchestrating the retained "load_SPR" step of the tgirke systempiperdata varseq finish finish workflow. It keeps the load SPR stage and the downstream handoff to `fastqc`. It tracks completion via `results/finish/load_SPR.done`.
metadata:
  workflow_id: tgirke-systempiperdata-varseq-finish
  workflow_name: tgirke systempiperdata varseq finish
  step_id: load_SPR
  step_name: load SPR
---

# Scope
Use this skill only for the `load_SPR` step in `tgirke-systempiperdata-varseq-finish`.

## Orchestration
- Upstream requirements: none
- Step file: `finish/tgirke-systempiperdata-varseq-finish/steps/load_SPR.smk`
- Config file: `finish/tgirke-systempiperdata-varseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/load_SPR.done`
- Representative outputs: `results/finish/load_SPR.done`
- Execution targets: `load_SPR`
- Downstream handoff: `fastqc`

## Guardrails
- Treat `results/finish/load_SPR.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/load_SPR.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `fastqc` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/load_SPR.done` exists and `fastqc` can proceed without re-running load SPR.
