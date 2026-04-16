---
name: finish-joncahn-epigeneticbutton-make_peak_stats
description: Use this skill when orchestrating the retained "make_peak_stats" step of the joncahn epigeneticbutton finish finish workflow. It keeps the make peak stats stage tied to upstream `best_peaks_pseudoreps` and the downstream handoff to `find_motifs_in_file`. It tracks completion via `results/finish/make_peak_stats.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: make_peak_stats
  step_name: make peak stats
---

# Scope
Use this skill only for the `make_peak_stats` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `best_peaks_pseudoreps`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/make_peak_stats.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/make_peak_stats.done`
- Representative outputs: `results/finish/make_peak_stats.done`
- Execution targets: `make_peak_stats`
- Downstream handoff: `find_motifs_in_file`

## Guardrails
- Treat `results/finish/make_peak_stats.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/make_peak_stats.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `find_motifs_in_file` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/make_peak_stats.done` exists and `find_motifs_in_file` can proceed without re-running make peak stats.
