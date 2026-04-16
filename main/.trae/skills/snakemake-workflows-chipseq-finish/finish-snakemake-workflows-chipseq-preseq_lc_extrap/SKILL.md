---
name: finish-snakemake-workflows-chipseq-preseq_lc_extrap
description: Use this skill when orchestrating the retained "preseq_lc_extrap" step of the snakemake workflows chipseq finish finish workflow. It keeps the preseq lc extrap stage tied to upstream `samtools_index` and the downstream handoff to `collect_multiple_metrics`. It tracks completion via `results/finish/preseq_lc_extrap.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: preseq_lc_extrap
  step_name: preseq lc extrap
---

# Scope
Use this skill only for the `preseq_lc_extrap` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `samtools_index`
- Step file: `finish/chipseq-finish/steps/preseq_lc_extrap.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/preseq_lc_extrap.done`
- Representative outputs: `results/finish/preseq_lc_extrap.done`
- Execution targets: `preseq_lc_extrap`
- Downstream handoff: `collect_multiple_metrics`

## Guardrails
- Treat `results/finish/preseq_lc_extrap.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/preseq_lc_extrap.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `collect_multiple_metrics` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/preseq_lc_extrap.done` exists and `collect_multiple_metrics` can proceed without re-running preseq lc extrap.
