---
name: finish-snakemake-workflows-chipseq-collect_multiple_metrics
description: Use this skill when orchestrating the retained "collect_multiple_metrics" step of the snakemake workflows chipseq finish finish workflow. It keeps the collect multiple metrics stage tied to upstream `preseq_lc_extrap` and the downstream handoff to `genomecov`. It tracks completion via `results/finish/collect_multiple_metrics.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: collect_multiple_metrics
  step_name: collect multiple metrics
---

# Scope
Use this skill only for the `collect_multiple_metrics` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `preseq_lc_extrap`
- Step file: `finish/chipseq-finish/steps/collect_multiple_metrics.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/collect_multiple_metrics.done`
- Representative outputs: `results/finish/collect_multiple_metrics.done`
- Execution targets: `collect_multiple_metrics`
- Downstream handoff: `genomecov`

## Guardrails
- Treat `results/finish/collect_multiple_metrics.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/collect_multiple_metrics.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `genomecov` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/collect_multiple_metrics.done` exists and `genomecov` can proceed without re-running collect multiple metrics.
