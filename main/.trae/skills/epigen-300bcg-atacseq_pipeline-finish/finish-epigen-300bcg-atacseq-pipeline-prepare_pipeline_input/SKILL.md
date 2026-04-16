---
name: finish-epigen-300bcg-atacseq-pipeline-prepare_pipeline_input
description: Use this skill when orchestrating the retained "prepare_pipeline_input" step of the epigen 300bcg atacseq_pipeline finish finish workflow. It keeps the Prepare Pipeline Input stage tied to upstream `parse_regulatory_build` and the downstream handoff to `run_pipeline`. It tracks completion via `results/finish/prepare_pipeline_input.done`.
metadata:
  workflow_id: epigen-300bcg-atacseq_pipeline-finish
  workflow_name: epigen 300bcg atacseq_pipeline finish
  step_id: prepare_pipeline_input
  step_name: Prepare Pipeline Input
---

# Scope
Use this skill only for the `prepare_pipeline_input` step in `epigen-300bcg-atacseq_pipeline-finish`.

## Orchestration
- Upstream requirements: `parse_regulatory_build`
- Step file: `finish/epigen-300bcg-atacseq_pipeline-finish/steps/prepare_pipeline_input.smk`
- Config file: `finish/epigen-300bcg-atacseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/prepare_pipeline_input.done`
- Representative outputs: `results/finish/prepare_pipeline_input.done`
- Execution targets: `prepare_pipeline_input`
- Downstream handoff: `run_pipeline`

## Guardrails
- Treat `results/finish/prepare_pipeline_input.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/prepare_pipeline_input.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `run_pipeline` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/prepare_pipeline_input.done` exists and `run_pipeline` can proceed without re-running Prepare Pipeline Input.
