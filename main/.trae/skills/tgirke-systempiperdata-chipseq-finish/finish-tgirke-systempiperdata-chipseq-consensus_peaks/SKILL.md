---
name: finish-tgirke-systempiperdata-chipseq-consensus_peaks
description: Use this skill when orchestrating the retained "consensus_peaks" step of the tgirke systempiperdata chipseq finish finish workflow. It keeps the consensus peaks stage tied to upstream `call_peaks_macs_withref` and the downstream handoff to `annotation_ChIPseeker`. It tracks completion via `results/finish/consensus_peaks.done`.
metadata:
  workflow_id: tgirke-systempiperdata-chipseq-finish
  workflow_name: tgirke systempiperdata chipseq finish
  step_id: consensus_peaks
  step_name: consensus peaks
---

# Scope
Use this skill only for the `consensus_peaks` step in `tgirke-systempiperdata-chipseq-finish`.

## Orchestration
- Upstream requirements: `call_peaks_macs_withref`
- Step file: `finish/tgirke-systempiperdata-chipseq-finish/steps/consensus_peaks.smk`
- Config file: `finish/tgirke-systempiperdata-chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/consensus_peaks.done`
- Representative outputs: `results/finish/consensus_peaks.done`
- Execution targets: `consensus_peaks`
- Downstream handoff: `annotation_ChIPseeker`

## Guardrails
- Treat `results/finish/consensus_peaks.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/consensus_peaks.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `annotation_ChIPseeker` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/consensus_peaks.done` exists and `annotation_ChIPseeker` can proceed without re-running consensus peaks.
