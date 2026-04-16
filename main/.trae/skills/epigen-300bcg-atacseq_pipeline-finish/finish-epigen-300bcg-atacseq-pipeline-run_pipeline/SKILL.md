---
name: finish-epigen-300bcg-atacseq-pipeline-run_pipeline
description: Use this skill when orchestrating the retained "run_pipeline" step of the epigen 300bcg atacseq_pipeline finish finish workflow. It keeps the Run Pipeline stage tied to upstream `prepare_pipeline_input` and the downstream handoff to `summarize_pipeline`. It tracks completion via `results/finish/run_pipeline.done`.
metadata:
  workflow_id: epigen-300bcg-atacseq_pipeline-finish
  workflow_name: epigen 300bcg atacseq_pipeline finish
  step_id: run_pipeline
  step_name: Run Pipeline
---

# Scope
Use this skill only for the `run_pipeline` step in `epigen-300bcg-atacseq_pipeline-finish`.

## Orchestration
- Upstream requirements: `prepare_pipeline_input`
- Step file: `finish/epigen-300bcg-atacseq_pipeline-finish/steps/run_pipeline.smk`
- Config file: `finish/epigen-300bcg-atacseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/run_pipeline.done`
- Representative outputs: `results/finish/run_pipeline.done`
- Execution targets: `run_pipeline`
- Downstream handoff: `summarize_pipeline`

## Guardrails
- Treat `results/finish/run_pipeline.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/run_pipeline.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `summarize_pipeline` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/run_pipeline.done` exists and `summarize_pipeline` can proceed without re-running Run Pipeline.
