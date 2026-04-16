---
name: finish-tgirke-systempiperdata-riboseq-coverage_combined
description: Use this skill when orchestrating the retained "coverage_combined" step of the tgirke systempiperdata riboseq finish finish workflow. It keeps the coverage combined stage tied to upstream `coverage_upstream_downstream` and the downstream handoff to `coverage_nuc_level`. It tracks completion via `results/finish/coverage_combined.done`.
metadata:
  workflow_id: tgirke-systempiperdata-riboseq-finish
  workflow_name: tgirke systempiperdata riboseq finish
  step_id: coverage_combined
  step_name: coverage combined
---

# Scope
Use this skill only for the `coverage_combined` step in `tgirke-systempiperdata-riboseq-finish`.

## Orchestration
- Upstream requirements: `coverage_upstream_downstream`
- Step file: `finish/tgirke-systempiperdata-riboseq-finish/steps/coverage_combined.smk`
- Config file: `finish/tgirke-systempiperdata-riboseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/coverage_combined.done`
- Representative outputs: `results/finish/coverage_combined.done`
- Execution targets: `coverage_combined`
- Downstream handoff: `coverage_nuc_level`

## Guardrails
- Treat `results/finish/coverage_combined.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/coverage_combined.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `coverage_nuc_level` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/coverage_combined.done` exists and `coverage_nuc_level` can proceed without re-running coverage combined.
