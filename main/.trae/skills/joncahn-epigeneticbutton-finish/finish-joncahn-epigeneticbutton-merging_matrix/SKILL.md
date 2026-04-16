---
name: finish-joncahn-epigeneticbutton-merging_matrix
description: Use this skill when orchestrating the retained "merging_matrix" step of the joncahn epigeneticbutton finish finish workflow. It keeps the merging matrix stage tied to upstream `making_stranded_matrix_on_targetfile` and the downstream handoff to `computing_matrix_scales`. It tracks completion via `results/finish/merging_matrix.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: merging_matrix
  step_name: merging matrix
---

# Scope
Use this skill only for the `merging_matrix` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `making_stranded_matrix_on_targetfile`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/merging_matrix.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/merging_matrix.done`
- Representative outputs: `results/finish/merging_matrix.done`
- Execution targets: `merging_matrix`
- Downstream handoff: `computing_matrix_scales`

## Guardrails
- Treat `results/finish/merging_matrix.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/merging_matrix.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `computing_matrix_scales` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/merging_matrix.done` exists and `computing_matrix_scales` can proceed without re-running merging matrix.
