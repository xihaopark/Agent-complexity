---
name: finish-lwang-genomics-ngs-pipeline-sn-chip-seq-call_peaks
description: Use this skill when orchestrating the retained "call_peaks" step of the lwang genomics ngs_pipeline_sn chip_seq finish finish workflow. It keeps the call peaks stage tied to upstream `bam_coverage` and the downstream handoff to `multiqc`. It tracks completion via `results/finish/call_peaks.done`.
metadata:
  workflow_id: lwang-genomics-ngs_pipeline_sn-chip_seq-finish
  workflow_name: lwang genomics ngs_pipeline_sn chip_seq finish
  step_id: call_peaks
  step_name: call peaks
---

# Scope
Use this skill only for the `call_peaks` step in `lwang-genomics-ngs_pipeline_sn-chip_seq-finish`.

## Orchestration
- Upstream requirements: `bam_coverage`
- Step file: `finish/lwang-genomics-ngs_pipeline_sn-chip_seq-finish/steps/call_peaks.smk`
- Config file: `finish/lwang-genomics-ngs_pipeline_sn-chip_seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/call_peaks.done`
- Representative outputs: `results/finish/call_peaks.done`
- Execution targets: `call_peaks`
- Downstream handoff: `multiqc`

## Guardrails
- Treat `results/finish/call_peaks.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/call_peaks.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `multiqc` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/call_peaks.done` exists and `multiqc` can proceed without re-running call peaks.
