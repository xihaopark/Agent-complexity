---
name: finish-tgirke-systempiperdata-rnaseq-heatmap
description: Use this skill when orchestrating the retained "heatmap" step of the tgirke systempiperdata rnaseq finish finish workflow. It keeps the heatmap stage tied to upstream `go_plot` and the downstream handoff to `sessionInfo`. It tracks completion via `results/finish/heatmap.done`.
metadata:
  workflow_id: tgirke-systempiperdata-rnaseq-finish
  workflow_name: tgirke systempiperdata rnaseq finish
  step_id: heatmap
  step_name: heatmap
---

# Scope
Use this skill only for the `heatmap` step in `tgirke-systempiperdata-rnaseq-finish`.

## Orchestration
- Upstream requirements: `go_plot`
- Step file: `finish/tgirke-systempiperdata-rnaseq-finish/steps/heatmap.smk`
- Config file: `finish/tgirke-systempiperdata-rnaseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/heatmap.done`
- Representative outputs: `results/finish/heatmap.done`
- Execution targets: `heatmap`
- Downstream handoff: `sessionInfo`

## Guardrails
- Treat `results/finish/heatmap.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/heatmap.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `sessionInfo` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/heatmap.done` exists and `sessionInfo` can proceed without re-running heatmap.
