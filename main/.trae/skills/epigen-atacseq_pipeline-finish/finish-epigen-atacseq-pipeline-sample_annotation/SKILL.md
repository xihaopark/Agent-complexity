---
name: finish-epigen-atacseq-pipeline-sample_annotation
description: Use this skill when orchestrating the retained "sample_annotation" step of the epigen atacseq_pipeline finish finish workflow. It keeps the sample annotation stage tied to upstream `plot_sample_annotation` and the downstream handoff to `get_promoter_regions`. It tracks completion via `results/finish/sample_annotation.done`.
metadata:
  workflow_id: epigen-atacseq_pipeline-finish
  workflow_name: epigen atacseq_pipeline finish
  step_id: sample_annotation
  step_name: sample annotation
---

# Scope
Use this skill only for the `sample_annotation` step in `epigen-atacseq_pipeline-finish`.

## Orchestration
- Upstream requirements: `plot_sample_annotation`
- Step file: `finish/epigen-atacseq_pipeline-finish/steps/sample_annotation.smk`
- Config file: `finish/epigen-atacseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/sample_annotation.done`
- Representative outputs: `results/finish/sample_annotation.done`
- Execution targets: `sample_annotation`
- Downstream handoff: `get_promoter_regions`

## Guardrails
- Treat `results/finish/sample_annotation.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/sample_annotation.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `get_promoter_regions` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/sample_annotation.done` exists and `get_promoter_regions` can proceed without re-running sample annotation.
