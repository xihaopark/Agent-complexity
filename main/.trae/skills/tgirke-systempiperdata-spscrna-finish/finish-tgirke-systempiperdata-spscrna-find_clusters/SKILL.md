---
name: finish-tgirke-systempiperdata-spscrna-find_clusters
description: Use this skill when orchestrating the retained "find_clusters" step of the tgirke systempiperdata spscrna finish finish workflow. It keeps the find clusters stage tied to upstream `choose_pcs` and the downstream handoff to `plot_cluster`. It tracks completion via `results/finish/find_clusters.done`.
metadata:
  workflow_id: tgirke-systempiperdata-spscrna-finish
  workflow_name: tgirke systempiperdata spscrna finish
  step_id: find_clusters
  step_name: find clusters
---

# Scope
Use this skill only for the `find_clusters` step in `tgirke-systempiperdata-spscrna-finish`.

## Orchestration
- Upstream requirements: `choose_pcs`
- Step file: `finish/tgirke-systempiperdata-spscrna-finish/steps/find_clusters.smk`
- Config file: `finish/tgirke-systempiperdata-spscrna-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/find_clusters.done`
- Representative outputs: `results/finish/find_clusters.done`
- Execution targets: `find_clusters`
- Downstream handoff: `plot_cluster`

## Guardrails
- Treat `results/finish/find_clusters.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/find_clusters.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plot_cluster` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/find_clusters.done` exists and `plot_cluster` can proceed without re-running find clusters.
