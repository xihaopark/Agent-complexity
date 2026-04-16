---
name: finish-snakemake-workflows-chipseq-macs2_callpeak_narrow
description: Use this skill when orchestrating the retained "macs2_callpeak_narrow" step of the snakemake workflows chipseq finish finish workflow. It keeps the macs2 callpeak narrow stage tied to upstream `macs2_callpeak_broad` and the downstream handoff to `peaks_count`. It tracks completion via `results/finish/macs2_callpeak_narrow.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: macs2_callpeak_narrow
  step_name: macs2 callpeak narrow
---

# Scope
Use this skill only for the `macs2_callpeak_narrow` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `macs2_callpeak_broad`
- Step file: `finish/chipseq-finish/steps/macs2_callpeak_narrow.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/macs2_callpeak_narrow.done`
- Representative outputs: `results/finish/macs2_callpeak_narrow.done`
- Execution targets: `macs2_callpeak_narrow`
- Downstream handoff: `peaks_count`

## Guardrails
- Treat `results/finish/macs2_callpeak_narrow.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/macs2_callpeak_narrow.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `peaks_count` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/macs2_callpeak_narrow.done` exists and `peaks_count` can proceed without re-running macs2 callpeak narrow.
