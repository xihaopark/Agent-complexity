---
name: finish-joncahn-epigeneticbutton-making_stranded_matrix_on_targetfile
description: Use this skill when orchestrating the retained "making_stranded_matrix_on_targetfile" step of the joncahn epigeneticbutton finish finish workflow. It keeps the making stranded matrix on targetfile stage tied to upstream `plotting_upset_regions` and the downstream handoff to `merging_matrix`. It tracks completion via `results/finish/making_stranded_matrix_on_targetfile.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: making_stranded_matrix_on_targetfile
  step_name: making stranded matrix on targetfile
---

# Scope
Use this skill only for the `making_stranded_matrix_on_targetfile` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `plotting_upset_regions`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/making_stranded_matrix_on_targetfile.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/making_stranded_matrix_on_targetfile.done`
- Representative outputs: `results/finish/making_stranded_matrix_on_targetfile.done`
- Execution targets: `making_stranded_matrix_on_targetfile`
- Downstream handoff: `merging_matrix`

## Guardrails
- Treat `results/finish/making_stranded_matrix_on_targetfile.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/making_stranded_matrix_on_targetfile.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `merging_matrix` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/making_stranded_matrix_on_targetfile.done` exists and `merging_matrix` can proceed without re-running making stranded matrix on targetfile.
