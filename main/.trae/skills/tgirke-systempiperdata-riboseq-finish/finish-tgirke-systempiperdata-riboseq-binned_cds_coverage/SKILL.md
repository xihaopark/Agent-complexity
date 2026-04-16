---
name: finish-tgirke-systempiperdata-riboseq-binned_cds_coverage
description: Use this skill when orchestrating the retained "binned_CDS_coverage" step of the tgirke systempiperdata riboseq finish finish workflow. It keeps the binned CDS coverage stage tied to upstream `pred_sORFs` and the downstream handoff to `coverage_upstream_downstream`. It tracks completion via `results/finish/binned_CDS_coverage.done`.
metadata:
  workflow_id: tgirke-systempiperdata-riboseq-finish
  workflow_name: tgirke systempiperdata riboseq finish
  step_id: binned_CDS_coverage
  step_name: binned CDS coverage
---

# Scope
Use this skill only for the `binned_CDS_coverage` step in `tgirke-systempiperdata-riboseq-finish`.

## Orchestration
- Upstream requirements: `pred_sORFs`
- Step file: `finish/tgirke-systempiperdata-riboseq-finish/steps/binned_CDS_coverage.smk`
- Config file: `finish/tgirke-systempiperdata-riboseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/binned_CDS_coverage.done`
- Representative outputs: `results/finish/binned_CDS_coverage.done`
- Execution targets: `binned_CDS_coverage`
- Downstream handoff: `coverage_upstream_downstream`

## Guardrails
- Treat `results/finish/binned_CDS_coverage.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/binned_CDS_coverage.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `coverage_upstream_downstream` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/binned_CDS_coverage.done` exists and `coverage_upstream_downstream` can proceed without re-running binned CDS coverage.
