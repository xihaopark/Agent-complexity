---
name: finish-snakemake-workflows-single-cell-rna-seq-plot_expression
description: Use this skill when orchestrating the retained "plot_expression" step of the snakemake workflows single cell rna seq finish finish workflow. It keeps the plot expression stage tied to upstream `edger` and the downstream handoff to `all`. It tracks completion via `results/finish/plot_expression.done`.
metadata:
  workflow_id: single-cell-rna-seq-finish
  workflow_name: snakemake workflows single cell rna seq finish
  step_id: plot_expression
  step_name: plot expression
---

# Scope
Use this skill only for the `plot_expression` step in `single-cell-rna-seq-finish`.

## Orchestration
- Upstream requirements: `edger`
- Step file: `finish/single-cell-rna-seq-finish/steps/plot_expression.smk`
- Config file: `finish/single-cell-rna-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plot_expression.done`
- Representative outputs: `results/finish/plot_expression.done`
- Execution targets: `plot_expression`
- Downstream handoff: `all`

## Guardrails
- Treat `results/finish/plot_expression.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plot_expression.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `all` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plot_expression.done` exists and `all` can proceed without re-running plot expression.
