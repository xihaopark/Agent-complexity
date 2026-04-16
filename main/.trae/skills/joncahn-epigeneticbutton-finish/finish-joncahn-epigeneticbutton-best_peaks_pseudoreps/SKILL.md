---
name: finish-joncahn-epigeneticbutton-best_peaks_pseudoreps
description: Use this skill when orchestrating the retained "best_peaks_pseudoreps" step of the joncahn epigeneticbutton finish finish workflow. It keeps the best peaks pseudoreps stage tied to upstream `create_empty_file` and the downstream handoff to `make_peak_stats`. It tracks completion via `results/finish/best_peaks_pseudoreps.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: best_peaks_pseudoreps
  step_name: best peaks pseudoreps
---

# Scope
Use this skill only for the `best_peaks_pseudoreps` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `create_empty_file`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/best_peaks_pseudoreps.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/best_peaks_pseudoreps.done`
- Representative outputs: `results/finish/best_peaks_pseudoreps.done`
- Execution targets: `best_peaks_pseudoreps`
- Downstream handoff: `make_peak_stats`

## Guardrails
- Treat `results/finish/best_peaks_pseudoreps.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/best_peaks_pseudoreps.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `make_peak_stats` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/best_peaks_pseudoreps.done` exists and `make_peak_stats` can proceed without re-running best peaks pseudoreps.
