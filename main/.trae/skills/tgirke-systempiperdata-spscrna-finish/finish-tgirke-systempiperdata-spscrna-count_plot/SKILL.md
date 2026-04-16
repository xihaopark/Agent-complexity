---
name: finish-tgirke-systempiperdata-spscrna-count_plot
description: Use this skill when orchestrating the retained "count_plot" step of the tgirke systempiperdata spscrna finish finish workflow. It keeps the count plot stage tied to upstream `load_data` and the downstream handoff to `create_seurat`. It tracks completion via `results/finish/count_plot.done`.
metadata:
  workflow_id: tgirke-systempiperdata-spscrna-finish
  workflow_name: tgirke systempiperdata spscrna finish
  step_id: count_plot
  step_name: count plot
---

# Scope
Use this skill only for the `count_plot` step in `tgirke-systempiperdata-spscrna-finish`.

## Orchestration
- Upstream requirements: `load_data`
- Step file: `finish/tgirke-systempiperdata-spscrna-finish/steps/count_plot.smk`
- Config file: `finish/tgirke-systempiperdata-spscrna-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/count_plot.done`
- Representative outputs: `results/finish/count_plot.done`
- Execution targets: `count_plot`
- Downstream handoff: `create_seurat`

## Guardrails
- Treat `results/finish/count_plot.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/count_plot.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `create_seurat` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/count_plot.done` exists and `create_seurat` can proceed without re-running count plot.
