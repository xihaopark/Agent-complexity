---
name: finish-tgirke-systempiperdata-riboseq-coverage_upstream_downstream
description: Use this skill when orchestrating the retained "coverage_upstream_downstream" step of the tgirke systempiperdata riboseq finish finish workflow. It keeps the coverage upstream downstream stage tied to upstream `binned_CDS_coverage` and the downstream handoff to `coverage_combined`. It tracks completion via `results/finish/coverage_upstream_downstream.done`.
metadata:
  workflow_id: tgirke-systempiperdata-riboseq-finish
  workflow_name: tgirke systempiperdata riboseq finish
  step_id: coverage_upstream_downstream
  step_name: coverage upstream downstream
---

# Scope
Use this skill only for the `coverage_upstream_downstream` step in `tgirke-systempiperdata-riboseq-finish`.

## Orchestration
- Upstream requirements: `binned_CDS_coverage`
- Step file: `finish/tgirke-systempiperdata-riboseq-finish/steps/coverage_upstream_downstream.smk`
- Config file: `finish/tgirke-systempiperdata-riboseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/coverage_upstream_downstream.done`
- Representative outputs: `results/finish/coverage_upstream_downstream.done`
- Execution targets: `coverage_upstream_downstream`
- Downstream handoff: `coverage_combined`

## Guardrails
- Treat `results/finish/coverage_upstream_downstream.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/coverage_upstream_downstream.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `coverage_combined` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/coverage_upstream_downstream.done` exists and `coverage_combined` can proceed without re-running coverage upstream downstream.
