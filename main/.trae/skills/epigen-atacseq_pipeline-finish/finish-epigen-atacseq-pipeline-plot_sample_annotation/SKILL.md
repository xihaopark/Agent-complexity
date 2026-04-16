---
name: finish-epigen-atacseq-pipeline-plot_sample_annotation
description: Use this skill when orchestrating the retained "plot_sample_annotation" step of the epigen atacseq_pipeline finish finish workflow. It keeps the plot sample annotation stage tied to upstream `multiqc` and the downstream handoff to `sample_annotation`. It tracks completion via `results/finish/plot_sample_annotation.done`.
metadata:
  workflow_id: epigen-atacseq_pipeline-finish
  workflow_name: epigen atacseq_pipeline finish
  step_id: plot_sample_annotation
  step_name: plot sample annotation
---

# Scope
Use this skill only for the `plot_sample_annotation` step in `epigen-atacseq_pipeline-finish`.

## Orchestration
- Upstream requirements: `multiqc`
- Step file: `finish/epigen-atacseq_pipeline-finish/steps/plot_sample_annotation.smk`
- Config file: `finish/epigen-atacseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plot_sample_annotation.done`
- Representative outputs: `results/finish/plot_sample_annotation.done`
- Execution targets: `plot_sample_annotation`
- Downstream handoff: `sample_annotation`

## Guardrails
- Treat `results/finish/plot_sample_annotation.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plot_sample_annotation.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `sample_annotation` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plot_sample_annotation.done` exists and `sample_annotation` can proceed without re-running plot sample annotation.
