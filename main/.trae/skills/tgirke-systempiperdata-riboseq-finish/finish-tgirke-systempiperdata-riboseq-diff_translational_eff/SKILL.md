---
name: finish-tgirke-systempiperdata-riboseq-diff_translational_eff
description: Use this skill when orchestrating the retained "diff_translational_eff" step of the tgirke systempiperdata riboseq finish finish workflow. It keeps the diff translational eff stage tied to upstream `diff_loading` and the downstream handoff to `heatmap`. It tracks completion via `results/finish/diff_translational_eff.done`.
metadata:
  workflow_id: tgirke-systempiperdata-riboseq-finish
  workflow_name: tgirke systempiperdata riboseq finish
  step_id: diff_translational_eff
  step_name: diff translational eff
---

# Scope
Use this skill only for the `diff_translational_eff` step in `tgirke-systempiperdata-riboseq-finish`.

## Orchestration
- Upstream requirements: `diff_loading`
- Step file: `finish/tgirke-systempiperdata-riboseq-finish/steps/diff_translational_eff.smk`
- Config file: `finish/tgirke-systempiperdata-riboseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/diff_translational_eff.done`
- Representative outputs: `results/finish/diff_translational_eff.done`
- Execution targets: `diff_translational_eff`
- Downstream handoff: `heatmap`

## Guardrails
- Treat `results/finish/diff_translational_eff.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/diff_translational_eff.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `heatmap` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/diff_translational_eff.done` exists and `heatmap` can proceed without re-running diff translational eff.
