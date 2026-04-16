---
name: finish-tgirke-systempiperdata-rnaseq-go_plot
description: Use this skill when orchestrating the retained "go_plot" step of the tgirke systempiperdata rnaseq finish finish workflow. It keeps the go plot stage tied to upstream `go_enrich` and the downstream handoff to `heatmap`. It tracks completion via `results/finish/go_plot.done`.
metadata:
  workflow_id: tgirke-systempiperdata-rnaseq-finish
  workflow_name: tgirke systempiperdata rnaseq finish
  step_id: go_plot
  step_name: go plot
---

# Scope
Use this skill only for the `go_plot` step in `tgirke-systempiperdata-rnaseq-finish`.

## Orchestration
- Upstream requirements: `go_enrich`
- Step file: `finish/tgirke-systempiperdata-rnaseq-finish/steps/go_plot.smk`
- Config file: `finish/tgirke-systempiperdata-rnaseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/go_plot.done`
- Representative outputs: `results/finish/go_plot.done`
- Execution targets: `go_plot`
- Downstream handoff: `heatmap`

## Guardrails
- Treat `results/finish/go_plot.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/go_plot.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `heatmap` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/go_plot.done` exists and `heatmap` can proceed without re-running go plot.
