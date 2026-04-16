---
name: finish-tgirke-systempiperdata-riboseq-diff_loading
description: Use this skill when orchestrating the retained "diff_loading" step of the tgirke systempiperdata riboseq finish finish workflow. It keeps the diff loading stage tied to upstream `go_plot` and the downstream handoff to `diff_translational_eff`. It tracks completion via `results/finish/diff_loading.done`.
metadata:
  workflow_id: tgirke-systempiperdata-riboseq-finish
  workflow_name: tgirke systempiperdata riboseq finish
  step_id: diff_loading
  step_name: diff loading
---

# Scope
Use this skill only for the `diff_loading` step in `tgirke-systempiperdata-riboseq-finish`.

## Orchestration
- Upstream requirements: `go_plot`
- Step file: `finish/tgirke-systempiperdata-riboseq-finish/steps/diff_loading.smk`
- Config file: `finish/tgirke-systempiperdata-riboseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/diff_loading.done`
- Representative outputs: `results/finish/diff_loading.done`
- Execution targets: `diff_loading`
- Downstream handoff: `diff_translational_eff`

## Guardrails
- Treat `results/finish/diff_loading.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/diff_loading.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `diff_translational_eff` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/diff_loading.done` exists and `diff_translational_eff` can proceed without re-running diff loading.
