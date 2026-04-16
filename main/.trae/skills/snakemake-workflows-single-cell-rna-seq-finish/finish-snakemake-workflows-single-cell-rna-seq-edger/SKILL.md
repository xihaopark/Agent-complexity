---
name: finish-snakemake-workflows-single-cell-rna-seq-edger
description: Use this skill when orchestrating the retained "edger" step of the snakemake workflows single cell rna seq finish finish workflow. It keeps the edger stage tied to upstream `plot_celltype_expressions` and the downstream handoff to `plot_expression`. It tracks completion via `results/finish/edger.done`.
metadata:
  workflow_id: single-cell-rna-seq-finish
  workflow_name: snakemake workflows single cell rna seq finish
  step_id: edger
  step_name: edger
---

# Scope
Use this skill only for the `edger` step in `single-cell-rna-seq-finish`.

## Orchestration
- Upstream requirements: `plot_celltype_expressions`
- Step file: `finish/single-cell-rna-seq-finish/steps/edger.smk`
- Config file: `finish/single-cell-rna-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/edger.done`
- Representative outputs: `results/finish/edger.done`
- Execution targets: `edger`
- Downstream handoff: `plot_expression`

## Guardrails
- Treat `results/finish/edger.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/edger.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plot_expression` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/edger.done` exists and `plot_expression` can proceed without re-running edger.
