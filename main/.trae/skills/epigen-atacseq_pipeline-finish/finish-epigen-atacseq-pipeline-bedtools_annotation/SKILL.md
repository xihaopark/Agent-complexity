---
name: finish-epigen-atacseq-pipeline-bedtools_annotation
description: Use this skill when orchestrating the retained "bedtools_annotation" step of the epigen atacseq_pipeline finish finish workflow. It keeps the bedtools annotation stage tied to upstream `homer_region_annotation` and the downstream handoff to `region_annotation_aggregate`. It tracks completion via `results/finish/bedtools_annotation.done`.
metadata:
  workflow_id: epigen-atacseq_pipeline-finish
  workflow_name: epigen atacseq_pipeline finish
  step_id: bedtools_annotation
  step_name: bedtools annotation
---

# Scope
Use this skill only for the `bedtools_annotation` step in `epigen-atacseq_pipeline-finish`.

## Orchestration
- Upstream requirements: `homer_region_annotation`
- Step file: `finish/epigen-atacseq_pipeline-finish/steps/bedtools_annotation.smk`
- Config file: `finish/epigen-atacseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/bedtools_annotation.done`
- Representative outputs: `results/finish/bedtools_annotation.done`
- Execution targets: `bedtools_annotation`
- Downstream handoff: `region_annotation_aggregate`

## Guardrails
- Treat `results/finish/bedtools_annotation.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/bedtools_annotation.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `region_annotation_aggregate` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/bedtools_annotation.done` exists and `region_annotation_aggregate` can proceed without re-running bedtools annotation.
