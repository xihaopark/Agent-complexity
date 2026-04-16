---
name: finish-tgirke-systempiperdata-chipseq-annotation_chipseeker
description: Use this skill when orchestrating the retained "annotation_ChIPseeker" step of the tgirke systempiperdata chipseq finish finish workflow. It keeps the annotation ChIPseeker stage tied to upstream `consensus_peaks` and the downstream handoff to `ChIPseeker_plots`. It tracks completion via `results/finish/annotation_ChIPseeker.done`.
metadata:
  workflow_id: tgirke-systempiperdata-chipseq-finish
  workflow_name: tgirke systempiperdata chipseq finish
  step_id: annotation_ChIPseeker
  step_name: annotation ChIPseeker
---

# Scope
Use this skill only for the `annotation_ChIPseeker` step in `tgirke-systempiperdata-chipseq-finish`.

## Orchestration
- Upstream requirements: `consensus_peaks`
- Step file: `finish/tgirke-systempiperdata-chipseq-finish/steps/annotation_ChIPseeker.smk`
- Config file: `finish/tgirke-systempiperdata-chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/annotation_ChIPseeker.done`
- Representative outputs: `results/finish/annotation_ChIPseeker.done`
- Execution targets: `annotation_ChIPseeker`
- Downstream handoff: `ChIPseeker_plots`

## Guardrails
- Treat `results/finish/annotation_ChIPseeker.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/annotation_ChIPseeker.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ChIPseeker_plots` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/annotation_ChIPseeker.done` exists and `ChIPseeker_plots` can proceed without re-running annotation ChIPseeker.
