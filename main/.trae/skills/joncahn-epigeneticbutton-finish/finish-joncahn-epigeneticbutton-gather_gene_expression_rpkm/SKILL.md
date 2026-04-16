---
name: finish-joncahn-epigeneticbutton-gather_gene_expression_rpkm
description: Use this skill when orchestrating the retained "gather_gene_expression_rpkm" step of the joncahn epigeneticbutton finish finish workflow. It keeps the gather gene expression rpkm stage tied to upstream `call_all_DEGs` and the downstream handoff to `plot_expression_levels`. It tracks completion via `results/finish/gather_gene_expression_rpkm.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: gather_gene_expression_rpkm
  step_name: gather gene expression rpkm
---

# Scope
Use this skill only for the `gather_gene_expression_rpkm` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `call_all_DEGs`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/gather_gene_expression_rpkm.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/gather_gene_expression_rpkm.done`
- Representative outputs: `results/finish/gather_gene_expression_rpkm.done`
- Execution targets: `gather_gene_expression_rpkm`
- Downstream handoff: `plot_expression_levels`

## Guardrails
- Treat `results/finish/gather_gene_expression_rpkm.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/gather_gene_expression_rpkm.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plot_expression_levels` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/gather_gene_expression_rpkm.done` exists and `plot_expression_levels` can proceed without re-running gather gene expression rpkm.
