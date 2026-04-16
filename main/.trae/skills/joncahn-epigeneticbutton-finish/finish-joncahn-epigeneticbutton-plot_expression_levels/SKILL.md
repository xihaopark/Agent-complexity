---
name: finish-joncahn-epigeneticbutton-plot_expression_levels
description: Use this skill when orchestrating the retained "plot_expression_levels" step of the joncahn epigeneticbutton finish finish workflow. It keeps the plot expression levels stage tied to upstream `gather_gene_expression_rpkm` and the downstream handoff to `create_GO_database`. It tracks completion via `results/finish/plot_expression_levels.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: plot_expression_levels
  step_name: plot expression levels
---

# Scope
Use this skill only for the `plot_expression_levels` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `gather_gene_expression_rpkm`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/plot_expression_levels.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plot_expression_levels.done`
- Representative outputs: `results/finish/plot_expression_levels.done`
- Execution targets: `plot_expression_levels`
- Downstream handoff: `create_GO_database`

## Guardrails
- Treat `results/finish/plot_expression_levels.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plot_expression_levels.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `create_GO_database` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plot_expression_levels.done` exists and `create_GO_database` can proceed without re-running plot expression levels.
