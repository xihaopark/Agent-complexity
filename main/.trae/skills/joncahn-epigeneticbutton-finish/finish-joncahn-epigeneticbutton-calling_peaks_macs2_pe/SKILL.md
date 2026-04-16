---
name: finish-joncahn-epigeneticbutton-calling_peaks_macs2_pe
description: Use this skill when orchestrating the retained "calling_peaks_macs2_pe" step of the joncahn epigeneticbutton finish finish workflow. It keeps the calling peaks macs2 pe stage tied to upstream `make_fingerprint_plot` and the downstream handoff to `calling_peaks_macs2_se`. It tracks completion via `results/finish/calling_peaks_macs2_pe.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: calling_peaks_macs2_pe
  step_name: calling peaks macs2 pe
---

# Scope
Use this skill only for the `calling_peaks_macs2_pe` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `make_fingerprint_plot`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/calling_peaks_macs2_pe.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/calling_peaks_macs2_pe.done`
- Representative outputs: `results/finish/calling_peaks_macs2_pe.done`
- Execution targets: `calling_peaks_macs2_pe`
- Downstream handoff: `calling_peaks_macs2_se`

## Guardrails
- Treat `results/finish/calling_peaks_macs2_pe.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/calling_peaks_macs2_pe.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `calling_peaks_macs2_se` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/calling_peaks_macs2_pe.done` exists and `calling_peaks_macs2_se` can proceed without re-running calling peaks macs2 pe.
