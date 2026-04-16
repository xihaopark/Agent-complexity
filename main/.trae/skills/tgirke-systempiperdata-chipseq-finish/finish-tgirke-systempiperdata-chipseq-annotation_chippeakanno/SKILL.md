---
name: finish-tgirke-systempiperdata-chipseq-annotation_chippeakanno
description: Use this skill when orchestrating the retained "annotation_ChIPpeakAnno" step of the tgirke systempiperdata chipseq finish finish workflow. It keeps the annotation ChIPpeakAnno stage tied to upstream `ChIPseeker_plots` and the downstream handoff to `count_peak_ranges`. It tracks completion via `results/finish/annotation_ChIPpeakAnno.done`.
metadata:
  workflow_id: tgirke-systempiperdata-chipseq-finish
  workflow_name: tgirke systempiperdata chipseq finish
  step_id: annotation_ChIPpeakAnno
  step_name: annotation ChIPpeakAnno
---

# Scope
Use this skill only for the `annotation_ChIPpeakAnno` step in `tgirke-systempiperdata-chipseq-finish`.

## Orchestration
- Upstream requirements: `ChIPseeker_plots`
- Step file: `finish/tgirke-systempiperdata-chipseq-finish/steps/annotation_ChIPpeakAnno.smk`
- Config file: `finish/tgirke-systempiperdata-chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/annotation_ChIPpeakAnno.done`
- Representative outputs: `results/finish/annotation_ChIPpeakAnno.done`
- Execution targets: `annotation_ChIPpeakAnno`
- Downstream handoff: `count_peak_ranges`

## Guardrails
- Treat `results/finish/annotation_ChIPpeakAnno.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/annotation_ChIPpeakAnno.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `count_peak_ranges` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/annotation_ChIPpeakAnno.done` exists and `count_peak_ranges` can proceed without re-running annotation ChIPpeakAnno.
