---
name: finish-tgirke-systempiperdata-spscrna-load_packages
description: Use this skill when orchestrating the retained "load_packages" step of the tgirke systempiperdata spscrna finish finish workflow. It keeps the load packages stage and the downstream handoff to `load_data`. It tracks completion via `results/finish/load_packages.done`.
metadata:
  workflow_id: tgirke-systempiperdata-spscrna-finish
  workflow_name: tgirke systempiperdata spscrna finish
  step_id: load_packages
  step_name: load packages
---

# Scope
Use this skill only for the `load_packages` step in `tgirke-systempiperdata-spscrna-finish`.

## Orchestration
- Upstream requirements: none
- Step file: `finish/tgirke-systempiperdata-spscrna-finish/steps/load_packages.smk`
- Config file: `finish/tgirke-systempiperdata-spscrna-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/load_packages.done`
- Representative outputs: `results/finish/load_packages.done`
- Execution targets: `load_packages`
- Downstream handoff: `load_data`

## Guardrails
- Treat `results/finish/load_packages.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/load_packages.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `load_data` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/load_packages.done` exists and `load_data` can proceed without re-running load packages.
