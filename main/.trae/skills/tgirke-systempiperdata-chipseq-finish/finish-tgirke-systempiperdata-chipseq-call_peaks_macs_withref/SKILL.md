---
name: finish-tgirke-systempiperdata-chipseq-call_peaks_macs_withref
description: Use this skill when orchestrating the retained "call_peaks_macs_withref" step of the tgirke systempiperdata chipseq finish finish workflow. It keeps the call peaks macs withref stage tied to upstream `call_peaks_macs_noref` and the downstream handoff to `consensus_peaks`. It tracks completion via `results/finish/call_peaks_macs_withref.done`.
metadata:
  workflow_id: tgirke-systempiperdata-chipseq-finish
  workflow_name: tgirke systempiperdata chipseq finish
  step_id: call_peaks_macs_withref
  step_name: call peaks macs withref
---

# Scope
Use this skill only for the `call_peaks_macs_withref` step in `tgirke-systempiperdata-chipseq-finish`.

## Orchestration
- Upstream requirements: `call_peaks_macs_noref`
- Step file: `finish/tgirke-systempiperdata-chipseq-finish/steps/call_peaks_macs_withref.smk`
- Config file: `finish/tgirke-systempiperdata-chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/call_peaks_macs_withref.done`
- Representative outputs: `results/finish/call_peaks_macs_withref.done`
- Execution targets: `call_peaks_macs_withref`
- Downstream handoff: `consensus_peaks`

## Guardrails
- Treat `results/finish/call_peaks_macs_withref.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/call_peaks_macs_withref.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `consensus_peaks` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/call_peaks_macs_withref.done` exists and `consensus_peaks` can proceed without re-running call peaks macs withref.
