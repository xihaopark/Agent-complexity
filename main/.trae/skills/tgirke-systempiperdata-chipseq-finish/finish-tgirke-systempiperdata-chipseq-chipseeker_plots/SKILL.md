---
name: finish-tgirke-systempiperdata-chipseq-chipseeker_plots
description: Use this skill when orchestrating the retained "ChIPseeker_plots" step of the tgirke systempiperdata chipseq finish finish workflow. It keeps the ChIPseeker plots stage tied to upstream `annotation_ChIPseeker` and the downstream handoff to `annotation_ChIPpeakAnno`. It tracks completion via `results/finish/ChIPseeker_plots.done`.
metadata:
  workflow_id: tgirke-systempiperdata-chipseq-finish
  workflow_name: tgirke systempiperdata chipseq finish
  step_id: ChIPseeker_plots
  step_name: ChIPseeker plots
---

# Scope
Use this skill only for the `ChIPseeker_plots` step in `tgirke-systempiperdata-chipseq-finish`.

## Orchestration
- Upstream requirements: `annotation_ChIPseeker`
- Step file: `finish/tgirke-systempiperdata-chipseq-finish/steps/ChIPseeker_plots.smk`
- Config file: `finish/tgirke-systempiperdata-chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ChIPseeker_plots.done`
- Representative outputs: `results/finish/ChIPseeker_plots.done`
- Execution targets: `ChIPseeker_plots`
- Downstream handoff: `annotation_ChIPpeakAnno`

## Guardrails
- Treat `results/finish/ChIPseeker_plots.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ChIPseeker_plots.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `annotation_ChIPpeakAnno` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ChIPseeker_plots.done` exists and `annotation_ChIPpeakAnno` can proceed without re-running ChIPseeker plots.
