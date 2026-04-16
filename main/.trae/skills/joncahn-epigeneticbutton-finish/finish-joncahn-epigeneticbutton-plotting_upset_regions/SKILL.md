---
name: finish-joncahn-epigeneticbutton-plotting_upset_regions
description: Use this skill when orchestrating the retained "plotting_upset_regions" step of the joncahn epigeneticbutton finish finish workflow. It keeps the plotting upset regions stage tied to upstream `get_annotations_for_bedfile` and the downstream handoff to `making_stranded_matrix_on_targetfile`. It tracks completion via `results/finish/plotting_upset_regions.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: plotting_upset_regions
  step_name: plotting upset regions
---

# Scope
Use this skill only for the `plotting_upset_regions` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `get_annotations_for_bedfile`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/plotting_upset_regions.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plotting_upset_regions.done`
- Representative outputs: `results/finish/plotting_upset_regions.done`
- Execution targets: `plotting_upset_regions`
- Downstream handoff: `making_stranded_matrix_on_targetfile`

## Guardrails
- Treat `results/finish/plotting_upset_regions.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plotting_upset_regions.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `making_stranded_matrix_on_targetfile` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plotting_upset_regions.done` exists and `making_stranded_matrix_on_targetfile` can proceed without re-running plotting upset regions.
