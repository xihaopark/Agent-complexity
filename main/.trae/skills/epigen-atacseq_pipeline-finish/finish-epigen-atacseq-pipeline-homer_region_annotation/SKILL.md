---
name: finish-epigen-atacseq-pipeline-homer_region_annotation
description: Use this skill when orchestrating the retained "homer_region_annotation" step of the epigen atacseq_pipeline finish finish workflow. It keeps the homer region annotation stage tied to upstream `uropa_reg` and the downstream handoff to `bedtools_annotation`. It tracks completion via `results/finish/homer_region_annotation.done`.
metadata:
  workflow_id: epigen-atacseq_pipeline-finish
  workflow_name: epigen atacseq_pipeline finish
  step_id: homer_region_annotation
  step_name: homer region annotation
---

# Scope
Use this skill only for the `homer_region_annotation` step in `epigen-atacseq_pipeline-finish`.

## Orchestration
- Upstream requirements: `uropa_reg`
- Step file: `finish/epigen-atacseq_pipeline-finish/steps/homer_region_annotation.smk`
- Config file: `finish/epigen-atacseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/homer_region_annotation.done`
- Representative outputs: `results/finish/homer_region_annotation.done`
- Execution targets: `homer_region_annotation`
- Downstream handoff: `bedtools_annotation`

## Guardrails
- Treat `results/finish/homer_region_annotation.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/homer_region_annotation.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `bedtools_annotation` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/homer_region_annotation.done` exists and `bedtools_annotation` can proceed without re-running homer region annotation.
