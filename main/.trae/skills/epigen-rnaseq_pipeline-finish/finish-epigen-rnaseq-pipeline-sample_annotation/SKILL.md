---
name: finish-epigen-rnaseq-pipeline-sample_annotation
description: Use this skill when orchestrating the retained "sample_annotation" step of the epigen rnaseq_pipeline finish finish workflow. It keeps the sample annotation stage tied to upstream `annotate_genes` and the downstream handoff to `all`. It tracks completion via `results/finish/sample_annotation.done`.
metadata:
  workflow_id: epigen-rnaseq_pipeline-finish
  workflow_name: epigen rnaseq_pipeline finish
  step_id: sample_annotation
  step_name: sample annotation
---

# Scope
Use this skill only for the `sample_annotation` step in `epigen-rnaseq_pipeline-finish`.

## Orchestration
- Upstream requirements: `annotate_genes`
- Step file: `finish/epigen-rnaseq_pipeline-finish/steps/sample_annotation.smk`
- Config file: `finish/epigen-rnaseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/sample_annotation.done`
- Representative outputs: `results/finish/sample_annotation.done`
- Execution targets: `sample_annotation`
- Downstream handoff: `all`

## Guardrails
- Treat `results/finish/sample_annotation.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/sample_annotation.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `all` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/sample_annotation.done` exists and `all` can proceed without re-running sample annotation.
