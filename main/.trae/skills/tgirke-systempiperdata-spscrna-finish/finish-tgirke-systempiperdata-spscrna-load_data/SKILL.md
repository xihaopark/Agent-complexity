---
name: finish-tgirke-systempiperdata-spscrna-load_data
description: Use this skill when orchestrating the retained "load_data" step of the tgirke systempiperdata spscrna finish finish workflow. It keeps the load data stage tied to upstream `load_packages` and the downstream handoff to `count_plot`. It tracks completion via `results/finish/load_data.done`.
metadata:
  workflow_id: tgirke-systempiperdata-spscrna-finish
  workflow_name: tgirke systempiperdata spscrna finish
  step_id: load_data
  step_name: load data
---

# Scope
Use this skill only for the `load_data` step in `tgirke-systempiperdata-spscrna-finish`.

## Orchestration
- Upstream requirements: `load_packages`
- Step file: `finish/tgirke-systempiperdata-spscrna-finish/steps/load_data.smk`
- Config file: `finish/tgirke-systempiperdata-spscrna-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/load_data.done`
- Representative outputs: `results/finish/load_data.done`
- Execution targets: `load_data`
- Downstream handoff: `count_plot`

## Guardrails
- Treat `results/finish/load_data.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/load_data.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `count_plot` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/load_data.done` exists and `count_plot` can proceed without re-running load data.
