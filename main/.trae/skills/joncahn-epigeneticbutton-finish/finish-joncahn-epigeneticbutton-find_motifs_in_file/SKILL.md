---
name: finish-joncahn-epigeneticbutton-find_motifs_in_file
description: Use this skill when orchestrating the retained "find_motifs_in_file" step of the joncahn epigeneticbutton finish finish workflow. It keeps the find motifs in file stage tied to upstream `make_peak_stats` and the downstream handoff to `perform_pairwise_diff_peaks`. It tracks completion via `results/finish/find_motifs_in_file.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: find_motifs_in_file
  step_name: find motifs in file
---

# Scope
Use this skill only for the `find_motifs_in_file` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `make_peak_stats`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/find_motifs_in_file.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/find_motifs_in_file.done`
- Representative outputs: `results/finish/find_motifs_in_file.done`
- Execution targets: `find_motifs_in_file`
- Downstream handoff: `perform_pairwise_diff_peaks`

## Guardrails
- Treat `results/finish/find_motifs_in_file.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/find_motifs_in_file.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `perform_pairwise_diff_peaks` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/find_motifs_in_file.done` exists and `perform_pairwise_diff_peaks` can proceed without re-running find motifs in file.
