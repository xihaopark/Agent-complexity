---
name: finish-epigen-rnaseq-pipeline-annotate_genes
description: Use this skill when orchestrating the retained "annotate_genes" step of the epigen rnaseq_pipeline finish finish workflow. It keeps the annotate genes stage tied to upstream `count_matrix` and the downstream handoff to `sample_annotation`. It tracks completion via `results/finish/annotate_genes.done`.
metadata:
  workflow_id: epigen-rnaseq_pipeline-finish
  workflow_name: epigen rnaseq_pipeline finish
  step_id: annotate_genes
  step_name: annotate genes
---

# Scope
Use this skill only for the `annotate_genes` step in `epigen-rnaseq_pipeline-finish`.

## Orchestration
- Upstream requirements: `count_matrix`
- Step file: `finish/epigen-rnaseq_pipeline-finish/steps/annotate_genes.smk`
- Config file: `finish/epigen-rnaseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/annotate_genes.done`
- Representative outputs: `results/finish/annotate_genes.done`
- Execution targets: `annotate_genes`
- Downstream handoff: `sample_annotation`

## Guardrails
- Treat `results/finish/annotate_genes.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/annotate_genes.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `sample_annotation` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/annotate_genes.done` exists and `sample_annotation` can proceed without re-running annotate genes.
