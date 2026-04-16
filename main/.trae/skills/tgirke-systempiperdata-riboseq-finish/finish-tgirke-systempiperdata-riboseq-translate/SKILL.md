---
name: finish-tgirke-systempiperdata-riboseq-translate
description: Use this skill when orchestrating the retained "translate" step of the tgirke systempiperdata riboseq finish finish workflow. It keeps the translate stage tied to upstream `scale_ranges` and the downstream handoff to `add_features`. It tracks completion via `results/finish/translate.done`.
metadata:
  workflow_id: tgirke-systempiperdata-riboseq-finish
  workflow_name: tgirke systempiperdata riboseq finish
  step_id: translate
  step_name: translate
---

# Scope
Use this skill only for the `translate` step in `tgirke-systempiperdata-riboseq-finish`.

## Orchestration
- Upstream requirements: `scale_ranges`
- Step file: `finish/tgirke-systempiperdata-riboseq-finish/steps/translate.smk`
- Config file: `finish/tgirke-systempiperdata-riboseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/translate.done`
- Representative outputs: `results/finish/translate.done`
- Execution targets: `translate`
- Downstream handoff: `add_features`

## Guardrails
- Treat `results/finish/translate.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/translate.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `add_features` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/translate.done` exists and `add_features` can proceed without re-running translate.
