---
name: finish-epigen-atacseq-pipeline-quantify_aggregate
description: Use this skill when orchestrating the retained "quantify_aggregate" step of the epigen atacseq_pipeline finish finish workflow. It keeps the quantify aggregate stage tied to upstream `quantify_counts_sample` and the downstream handoff to `homer_aggregate`. It tracks completion via `results/finish/quantify_aggregate.done`.
metadata:
  workflow_id: epigen-atacseq_pipeline-finish
  workflow_name: epigen atacseq_pipeline finish
  step_id: quantify_aggregate
  step_name: quantify aggregate
---

# Scope
Use this skill only for the `quantify_aggregate` step in `epigen-atacseq_pipeline-finish`.

## Orchestration
- Upstream requirements: `quantify_counts_sample`
- Step file: `finish/epigen-atacseq_pipeline-finish/steps/quantify_aggregate.smk`
- Config file: `finish/epigen-atacseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/quantify_aggregate.done`
- Representative outputs: `results/finish/quantify_aggregate.done`
- Execution targets: `quantify_aggregate`
- Downstream handoff: `homer_aggregate`

## Guardrails
- Treat `results/finish/quantify_aggregate.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/quantify_aggregate.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `homer_aggregate` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/quantify_aggregate.done` exists and `homer_aggregate` can proceed without re-running quantify aggregate.
