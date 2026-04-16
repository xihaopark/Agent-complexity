---
name: finish-tgirke-systempiperdata-riboseq-pred_sorfs
description: Use this skill when orchestrating the retained "pred_sORFs" step of the tgirke systempiperdata riboseq finish finish workflow. It keeps the pred sORFs stage tied to upstream `add_features` and the downstream handoff to `binned_CDS_coverage`. It tracks completion via `results/finish/pred_sORFs.done`.
metadata:
  workflow_id: tgirke-systempiperdata-riboseq-finish
  workflow_name: tgirke systempiperdata riboseq finish
  step_id: pred_sORFs
  step_name: pred sORFs
---

# Scope
Use this skill only for the `pred_sORFs` step in `tgirke-systempiperdata-riboseq-finish`.

## Orchestration
- Upstream requirements: `add_features`
- Step file: `finish/tgirke-systempiperdata-riboseq-finish/steps/pred_sORFs.smk`
- Config file: `finish/tgirke-systempiperdata-riboseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/pred_sORFs.done`
- Representative outputs: `results/finish/pred_sORFs.done`
- Execution targets: `pred_sORFs`
- Downstream handoff: `binned_CDS_coverage`

## Guardrails
- Treat `results/finish/pred_sORFs.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/pred_sORFs.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `binned_CDS_coverage` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/pred_sORFs.done` exists and `binned_CDS_coverage` can proceed without re-running pred sORFs.
