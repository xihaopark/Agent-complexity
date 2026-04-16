---
name: finish-tgirke-systempiperdata-riboseq-sessioninfo
description: Use this skill when orchestrating the retained "sessionInfo" step of the tgirke systempiperdata riboseq finish finish workflow. It keeps the sessionInfo stage tied to upstream `heatmap`. It tracks completion via `results/finish/sessionInfo.done`.
metadata:
  workflow_id: tgirke-systempiperdata-riboseq-finish
  workflow_name: tgirke systempiperdata riboseq finish
  step_id: sessionInfo
  step_name: sessionInfo
---

# Scope
Use this skill only for the `sessionInfo` step in `tgirke-systempiperdata-riboseq-finish`.

## Orchestration
- Upstream requirements: `heatmap`
- Step file: `finish/tgirke-systempiperdata-riboseq-finish/steps/sessionInfo.smk`
- Config file: `finish/tgirke-systempiperdata-riboseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/sessionInfo.done`
- Representative outputs: `results/finish/sessionInfo.done`
- Execution targets: `sessionInfo`
- Downstream handoff: none

## Guardrails
- Treat `results/finish/sessionInfo.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/sessionInfo.smk` so the step remains separable and replayable inside the finish workflow.

## Done Criteria
Mark this step complete only when `results/finish/sessionInfo.done` exists and matches the intended step boundary.
