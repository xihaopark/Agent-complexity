---
name: finish-tgirke-systempiperdata-spscrna-find_markers
description: Use this skill when orchestrating the retained "find_markers" step of the tgirke systempiperdata spscrna finish finish workflow. It keeps the find markers stage tied to upstream `plot_cluster` and the downstream handoff to `plot_markers`. It tracks completion via `results/finish/find_markers.done`.
metadata:
  workflow_id: tgirke-systempiperdata-spscrna-finish
  workflow_name: tgirke systempiperdata spscrna finish
  step_id: find_markers
  step_name: find markers
---

# Scope
Use this skill only for the `find_markers` step in `tgirke-systempiperdata-spscrna-finish`.

## Orchestration
- Upstream requirements: `plot_cluster`
- Step file: `finish/tgirke-systempiperdata-spscrna-finish/steps/find_markers.smk`
- Config file: `finish/tgirke-systempiperdata-spscrna-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/find_markers.done`
- Representative outputs: `results/finish/find_markers.done`
- Execution targets: `find_markers`
- Downstream handoff: `plot_markers`

## Guardrails
- Treat `results/finish/find_markers.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/find_markers.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plot_markers` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/find_markers.done` exists and `plot_markers` can proceed without re-running find markers.
