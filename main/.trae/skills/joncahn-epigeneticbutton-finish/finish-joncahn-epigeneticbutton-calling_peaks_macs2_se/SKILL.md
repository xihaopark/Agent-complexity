---
name: finish-joncahn-epigeneticbutton-calling_peaks_macs2_se
description: Use this skill when orchestrating the retained "calling_peaks_macs2_se" step of the joncahn epigeneticbutton finish finish workflow. It keeps the calling peaks macs2 se stage tied to upstream `calling_peaks_macs2_pe` and the downstream handoff to `idr_analysis_replicates`. It tracks completion via `results/finish/calling_peaks_macs2_se.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: calling_peaks_macs2_se
  step_name: calling peaks macs2 se
---

# Scope
Use this skill only for the `calling_peaks_macs2_se` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `calling_peaks_macs2_pe`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/calling_peaks_macs2_se.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/calling_peaks_macs2_se.done`
- Representative outputs: `results/finish/calling_peaks_macs2_se.done`
- Execution targets: `calling_peaks_macs2_se`
- Downstream handoff: `idr_analysis_replicates`

## Guardrails
- Treat `results/finish/calling_peaks_macs2_se.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/calling_peaks_macs2_se.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `idr_analysis_replicates` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/calling_peaks_macs2_se.done` exists and `idr_analysis_replicates` can proceed without re-running calling peaks macs2 se.
