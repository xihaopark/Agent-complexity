---
name: finish-tgirke-systempiperdata-riboseq-coverage_nuc_level
description: Use this skill when orchestrating the retained "coverage_nuc_level" step of the tgirke systempiperdata riboseq finish finish workflow. It keeps the coverage nuc level stage tied to upstream `coverage_combined` and the downstream handoff to `read_counting`. It tracks completion via `results/finish/coverage_nuc_level.done`.
metadata:
  workflow_id: tgirke-systempiperdata-riboseq-finish
  workflow_name: tgirke systempiperdata riboseq finish
  step_id: coverage_nuc_level
  step_name: coverage nuc level
---

# Scope
Use this skill only for the `coverage_nuc_level` step in `tgirke-systempiperdata-riboseq-finish`.

## Orchestration
- Upstream requirements: `coverage_combined`
- Step file: `finish/tgirke-systempiperdata-riboseq-finish/steps/coverage_nuc_level.smk`
- Config file: `finish/tgirke-systempiperdata-riboseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/coverage_nuc_level.done`
- Representative outputs: `results/finish/coverage_nuc_level.done`
- Execution targets: `coverage_nuc_level`
- Downstream handoff: `read_counting`

## Guardrails
- Treat `results/finish/coverage_nuc_level.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/coverage_nuc_level.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `read_counting` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/coverage_nuc_level.done` exists and `read_counting` can proceed without re-running coverage nuc level.
