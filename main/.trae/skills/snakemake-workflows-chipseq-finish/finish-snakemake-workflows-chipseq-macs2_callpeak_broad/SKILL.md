---
name: finish-snakemake-workflows-chipseq-macs2_callpeak_broad
description: Use this skill when orchestrating the retained "macs2_callpeak_broad" step of the snakemake workflows chipseq finish finish workflow. It keeps the macs2 callpeak broad stage tied to upstream `plot_fingerprint` and the downstream handoff to `macs2_callpeak_narrow`. It tracks completion via `results/finish/macs2_callpeak_broad.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: macs2_callpeak_broad
  step_name: macs2 callpeak broad
---

# Scope
Use this skill only for the `macs2_callpeak_broad` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `plot_fingerprint`
- Step file: `finish/chipseq-finish/steps/macs2_callpeak_broad.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/macs2_callpeak_broad.done`
- Representative outputs: `results/finish/macs2_callpeak_broad.done`
- Execution targets: `macs2_callpeak_broad`
- Downstream handoff: `macs2_callpeak_narrow`

## Guardrails
- Treat `results/finish/macs2_callpeak_broad.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/macs2_callpeak_broad.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `macs2_callpeak_narrow` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/macs2_callpeak_broad.done` exists and `macs2_callpeak_narrow` can proceed without re-running macs2 callpeak broad.
