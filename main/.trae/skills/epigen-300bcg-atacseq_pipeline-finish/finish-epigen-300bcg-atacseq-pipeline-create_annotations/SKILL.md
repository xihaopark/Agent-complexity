---
name: finish-epigen-300bcg-atacseq-pipeline-create_annotations
description: Use this skill when orchestrating the retained "create_annotations" step of the epigen 300bcg atacseq_pipeline finish finish workflow. It keeps the Create Annotations stage tied to upstream `summarize_pipeline` and the downstream handoff to `qc_stats`. It tracks completion via `results/finish/create_annotations.done`.
metadata:
  workflow_id: epigen-300bcg-atacseq_pipeline-finish
  workflow_name: epigen 300bcg atacseq_pipeline finish
  step_id: create_annotations
  step_name: Create Annotations
---

# Scope
Use this skill only for the `create_annotations` step in `epigen-300bcg-atacseq_pipeline-finish`.

## Orchestration
- Upstream requirements: `summarize_pipeline`
- Step file: `finish/epigen-300bcg-atacseq_pipeline-finish/steps/create_annotations.smk`
- Config file: `finish/epigen-300bcg-atacseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/create_annotations.done`
- Representative outputs: `results/finish/create_annotations.done`
- Execution targets: `create_annotations`
- Downstream handoff: `qc_stats`

## Guardrails
- Treat `results/finish/create_annotations.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/create_annotations.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `qc_stats` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/create_annotations.done` exists and `qc_stats` can proceed without re-running Create Annotations.
