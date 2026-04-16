---
name: finish-joncahn-epigeneticbutton-create_empty_file
description: Use this skill when orchestrating the retained "create_empty_file" step of the joncahn epigeneticbutton finish finish workflow. It keeps the create empty file stage tied to upstream `making_pseudo_replicates` and the downstream handoff to `best_peaks_pseudoreps`. It tracks completion via `results/finish/create_empty_file.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: create_empty_file
  step_name: create empty file
---

# Scope
Use this skill only for the `create_empty_file` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `making_pseudo_replicates`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/create_empty_file.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/create_empty_file.done`
- Representative outputs: `results/finish/create_empty_file.done`
- Execution targets: `create_empty_file`
- Downstream handoff: `best_peaks_pseudoreps`

## Guardrails
- Treat `results/finish/create_empty_file.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/create_empty_file.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `best_peaks_pseudoreps` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/create_empty_file.done` exists and `best_peaks_pseudoreps` can proceed without re-running create empty file.
