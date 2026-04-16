---
name: finish-tgirke-systempiperdata-chipseq-call_peaks_macs_noref
description: Use this skill when orchestrating the retained "call_peaks_macs_noref" step of the tgirke systempiperdata chipseq finish finish workflow. It keeps the call peaks macs noref stage tied to upstream `merge_bams` and the downstream handoff to `call_peaks_macs_withref`. It tracks completion via `results/finish/call_peaks_macs_noref.done`.
metadata:
  workflow_id: tgirke-systempiperdata-chipseq-finish
  workflow_name: tgirke systempiperdata chipseq finish
  step_id: call_peaks_macs_noref
  step_name: call peaks macs noref
---

# Scope
Use this skill only for the `call_peaks_macs_noref` step in `tgirke-systempiperdata-chipseq-finish`.

## Orchestration
- Upstream requirements: `merge_bams`
- Step file: `finish/tgirke-systempiperdata-chipseq-finish/steps/call_peaks_macs_noref.smk`
- Config file: `finish/tgirke-systempiperdata-chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/call_peaks_macs_noref.done`
- Representative outputs: `results/finish/call_peaks_macs_noref.done`
- Execution targets: `call_peaks_macs_noref`
- Downstream handoff: `call_peaks_macs_withref`

## Guardrails
- Treat `results/finish/call_peaks_macs_noref.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/call_peaks_macs_noref.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `call_peaks_macs_withref` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/call_peaks_macs_noref.done` exists and `call_peaks_macs_withref` can proceed without re-running call peaks macs noref.
