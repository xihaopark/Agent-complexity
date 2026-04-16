---
name: finish-tgirke-systempiperdata-spscrna-plot_cluster
description: Use this skill when orchestrating the retained "plot_cluster" step of the tgirke systempiperdata spscrna finish finish workflow. It keeps the plot cluster stage tied to upstream `find_clusters` and the downstream handoff to `find_markers`. It tracks completion via `results/finish/plot_cluster.done`.
metadata:
  workflow_id: tgirke-systempiperdata-spscrna-finish
  workflow_name: tgirke systempiperdata spscrna finish
  step_id: plot_cluster
  step_name: plot cluster
---

# Scope
Use this skill only for the `plot_cluster` step in `tgirke-systempiperdata-spscrna-finish`.

## Orchestration
- Upstream requirements: `find_clusters`
- Step file: `finish/tgirke-systempiperdata-spscrna-finish/steps/plot_cluster.smk`
- Config file: `finish/tgirke-systempiperdata-spscrna-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plot_cluster.done`
- Representative outputs: `results/finish/plot_cluster.done`
- Execution targets: `plot_cluster`
- Downstream handoff: `find_markers`

## Guardrails
- Treat `results/finish/plot_cluster.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plot_cluster.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `find_markers` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plot_cluster.done` exists and `find_markers` can proceed without re-running plot cluster.
