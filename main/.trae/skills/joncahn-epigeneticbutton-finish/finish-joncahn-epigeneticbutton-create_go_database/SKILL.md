---
name: finish-joncahn-epigeneticbutton-create_go_database
description: Use this skill when orchestrating the retained "create_GO_database" step of the joncahn epigeneticbutton finish finish workflow. It keeps the create GO database stage tied to upstream `plot_expression_levels` and the downstream handoff to `perform_GO_on_target_file`. It tracks completion via `results/finish/create_GO_database.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: create_GO_database
  step_name: create GO database
---

# Scope
Use this skill only for the `create_GO_database` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `plot_expression_levels`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/create_GO_database.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/create_GO_database.done`
- Representative outputs: `results/finish/create_GO_database.done`
- Execution targets: `create_GO_database`
- Downstream handoff: `perform_GO_on_target_file`

## Guardrails
- Treat `results/finish/create_GO_database.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/create_GO_database.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `perform_GO_on_target_file` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/create_GO_database.done` exists and `perform_GO_on_target_file` can proceed without re-running create GO database.
