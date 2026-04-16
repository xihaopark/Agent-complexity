---
name: finish-joncahn-epigeneticbutton-make_fingerprint_plot
description: Use this skill when orchestrating the retained "make_fingerprint_plot" step of the joncahn epigeneticbutton finish finish workflow. It keeps the make fingerprint plot stage tied to upstream `make_bigwig_chip` and the downstream handoff to `calling_peaks_macs2_pe`. It tracks completion via `results/finish/make_fingerprint_plot.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: make_fingerprint_plot
  step_name: make fingerprint plot
---

# Scope
Use this skill only for the `make_fingerprint_plot` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `make_bigwig_chip`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/make_fingerprint_plot.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/make_fingerprint_plot.done`
- Representative outputs: `results/finish/make_fingerprint_plot.done`
- Execution targets: `make_fingerprint_plot`
- Downstream handoff: `calling_peaks_macs2_pe`

## Guardrails
- Treat `results/finish/make_fingerprint_plot.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/make_fingerprint_plot.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `calling_peaks_macs2_pe` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/make_fingerprint_plot.done` exists and `calling_peaks_macs2_pe` can proceed without re-running make fingerprint plot.
