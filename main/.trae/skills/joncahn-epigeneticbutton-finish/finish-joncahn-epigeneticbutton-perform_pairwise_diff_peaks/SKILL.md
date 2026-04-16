---
name: finish-joncahn-epigeneticbutton-perform_pairwise_diff_peaks
description: Use this skill when orchestrating the retained "perform_pairwise_diff_peaks" step of the joncahn epigeneticbutton finish finish workflow. It keeps the perform pairwise diff peaks stage tied to upstream `find_motifs_in_file` and the downstream handoff to `all_chip`. It tracks completion via `results/finish/perform_pairwise_diff_peaks.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: perform_pairwise_diff_peaks
  step_name: perform pairwise diff peaks
---

# Scope
Use this skill only for the `perform_pairwise_diff_peaks` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `find_motifs_in_file`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/perform_pairwise_diff_peaks.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/perform_pairwise_diff_peaks.done`
- Representative outputs: `results/finish/perform_pairwise_diff_peaks.done`
- Execution targets: `perform_pairwise_diff_peaks`
- Downstream handoff: `all_chip`

## Guardrails
- Treat `results/finish/perform_pairwise_diff_peaks.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/perform_pairwise_diff_peaks.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `all_chip` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/perform_pairwise_diff_peaks.done` exists and `all_chip` can proceed without re-running perform pairwise diff peaks.
