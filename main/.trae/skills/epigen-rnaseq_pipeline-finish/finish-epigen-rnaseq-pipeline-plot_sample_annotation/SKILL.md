---
name: finish-epigen-rnaseq-pipeline-plot_sample_annotation
description: Use this skill when orchestrating the retained "plot_sample_annotation" step of the epigen rnaseq_pipeline finish finish workflow. It keeps the plot sample annotation stage tied to upstream `multiqc` and the downstream handoff to `check_read_type`. It tracks completion via `results/finish/plot_sample_annotation.done`.
metadata:
  workflow_id: epigen-rnaseq_pipeline-finish
  workflow_name: epigen rnaseq_pipeline finish
  step_id: plot_sample_annotation
  step_name: plot sample annotation
---

# Scope
Use this skill only for the `plot_sample_annotation` step in `epigen-rnaseq_pipeline-finish`.

## Orchestration
- Upstream requirements: `multiqc`
- Step file: `finish/epigen-rnaseq_pipeline-finish/steps/plot_sample_annotation.smk`
- Config file: `finish/epigen-rnaseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plot_sample_annotation.done`
- Representative outputs: `results/finish/plot_sample_annotation.done`
- Execution targets: `plot_sample_annotation`
- Downstream handoff: `check_read_type`

## Guardrails
- Treat `results/finish/plot_sample_annotation.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plot_sample_annotation.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `check_read_type` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plot_sample_annotation.done` exists and `check_read_type` can proceed without re-running plot sample annotation.
