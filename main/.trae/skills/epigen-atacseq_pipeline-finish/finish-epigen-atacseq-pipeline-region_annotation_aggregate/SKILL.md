---
name: finish-epigen-atacseq-pipeline-region_annotation_aggregate
description: Use this skill when orchestrating the retained "region_annotation_aggregate" step of the epigen atacseq_pipeline finish finish workflow. It keeps the region annotation aggregate stage tied to upstream `bedtools_annotation` and the downstream handoff to `all`. It tracks completion via `results/finish/region_annotation_aggregate.done`.
metadata:
  workflow_id: epigen-atacseq_pipeline-finish
  workflow_name: epigen atacseq_pipeline finish
  step_id: region_annotation_aggregate
  step_name: region annotation aggregate
---

# Scope
Use this skill only for the `region_annotation_aggregate` step in `epigen-atacseq_pipeline-finish`.

## Orchestration
- Upstream requirements: `bedtools_annotation`
- Step file: `finish/epigen-atacseq_pipeline-finish/steps/region_annotation_aggregate.smk`
- Config file: `finish/epigen-atacseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/region_annotation_aggregate.done`
- Representative outputs: `results/finish/region_annotation_aggregate.done`
- Execution targets: `region_annotation_aggregate`
- Downstream handoff: `all`

## Guardrails
- Treat `results/finish/region_annotation_aggregate.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/region_annotation_aggregate.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `all` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/region_annotation_aggregate.done` exists and `all` can proceed without re-running region annotation aggregate.
