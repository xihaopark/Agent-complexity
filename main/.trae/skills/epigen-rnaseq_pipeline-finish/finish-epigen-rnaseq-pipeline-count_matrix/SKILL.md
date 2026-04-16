---
name: finish-epigen-rnaseq-pipeline-count_matrix
description: Use this skill when orchestrating the retained "count_matrix" step of the epigen rnaseq_pipeline finish finish workflow. It keeps the count matrix stage tied to upstream `align` and the downstream handoff to `annotate_genes`. It tracks completion via `results/finish/count_matrix.done`.
metadata:
  workflow_id: epigen-rnaseq_pipeline-finish
  workflow_name: epigen rnaseq_pipeline finish
  step_id: count_matrix
  step_name: count matrix
---

# Scope
Use this skill only for the `count_matrix` step in `epigen-rnaseq_pipeline-finish`.

## Orchestration
- Upstream requirements: `align`
- Step file: `finish/epigen-rnaseq_pipeline-finish/steps/count_matrix.smk`
- Config file: `finish/epigen-rnaseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/count_matrix.done`
- Representative outputs: `results/finish/count_matrix.done`
- Execution targets: `count_matrix`
- Downstream handoff: `annotate_genes`

## Guardrails
- Treat `results/finish/count_matrix.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/count_matrix.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `annotate_genes` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/count_matrix.done` exists and `annotate_genes` can proceed without re-running count matrix.
