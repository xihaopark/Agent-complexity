---
name: finish-epigen-300bcg-atacseq-pipeline-summarize_pipeline
description: Use this skill when orchestrating the retained "summarize_pipeline" step of the epigen 300bcg atacseq_pipeline finish finish workflow. It keeps the Summarize Pipeline stage tied to upstream `run_pipeline` and the downstream handoff to `create_annotations`. It tracks completion via `results/finish/summarize_pipeline.done`.
metadata:
  workflow_id: epigen-300bcg-atacseq_pipeline-finish
  workflow_name: epigen 300bcg atacseq_pipeline finish
  step_id: summarize_pipeline
  step_name: Summarize Pipeline
---

# Scope
Use this skill only for the `summarize_pipeline` step in `epigen-300bcg-atacseq_pipeline-finish`.

## Orchestration
- Upstream requirements: `run_pipeline`
- Step file: `finish/epigen-300bcg-atacseq_pipeline-finish/steps/summarize_pipeline.smk`
- Config file: `finish/epigen-300bcg-atacseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/summarize_pipeline.done`
- Representative outputs: `results/finish/summarize_pipeline.done`
- Execution targets: `summarize_pipeline`
- Downstream handoff: `create_annotations`

## Guardrails
- Treat `results/finish/summarize_pipeline.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/summarize_pipeline.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `create_annotations` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/summarize_pipeline.done` exists and `create_annotations` can proceed without re-running Summarize Pipeline.
