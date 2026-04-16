---
name: finish-tgirke-systempiperdata-riboseq-add_features
description: Use this skill when orchestrating the retained "add_features" step of the tgirke systempiperdata riboseq finish finish workflow. It keeps the add features stage tied to upstream `translate` and the downstream handoff to `pred_sORFs`. It tracks completion via `results/finish/add_features.done`.
metadata:
  workflow_id: tgirke-systempiperdata-riboseq-finish
  workflow_name: tgirke systempiperdata riboseq finish
  step_id: add_features
  step_name: add features
---

# Scope
Use this skill only for the `add_features` step in `tgirke-systempiperdata-riboseq-finish`.

## Orchestration
- Upstream requirements: `translate`
- Step file: `finish/tgirke-systempiperdata-riboseq-finish/steps/add_features.smk`
- Config file: `finish/tgirke-systempiperdata-riboseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/add_features.done`
- Representative outputs: `results/finish/add_features.done`
- Execution targets: `add_features`
- Downstream handoff: `pred_sORFs`

## Guardrails
- Treat `results/finish/add_features.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/add_features.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `pred_sORFs` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/add_features.done` exists and `pred_sORFs` can proceed without re-running add features.
