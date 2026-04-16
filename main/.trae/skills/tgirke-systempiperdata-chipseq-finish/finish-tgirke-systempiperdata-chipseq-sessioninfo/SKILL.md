---
name: finish-tgirke-systempiperdata-chipseq-sessioninfo
description: Use this skill when orchestrating the retained "sessionInfo" step of the tgirke systempiperdata chipseq finish finish workflow. It keeps the sessionInfo stage tied to upstream `bcrank_enrich`. It tracks completion via `results/finish/sessionInfo.done`.
metadata:
  workflow_id: tgirke-systempiperdata-chipseq-finish
  workflow_name: tgirke systempiperdata chipseq finish
  step_id: sessionInfo
  step_name: sessionInfo
---

# Scope
Use this skill only for the `sessionInfo` step in `tgirke-systempiperdata-chipseq-finish`.

## Orchestration
- Upstream requirements: `bcrank_enrich`
- Step file: `finish/tgirke-systempiperdata-chipseq-finish/steps/sessionInfo.smk`
- Config file: `finish/tgirke-systempiperdata-chipseq-finish/config_basic/config.yaml`
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
