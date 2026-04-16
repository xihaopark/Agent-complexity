---
name: finish-epigen-atacseq-pipeline-homer_aggregate
description: Use this skill when orchestrating the retained "homer_aggregate" step of the epigen atacseq_pipeline finish finish workflow. It keeps the homer aggregate stage tied to upstream `quantify_aggregate` and the downstream handoff to `map_consensus_tss`. It tracks completion via `results/finish/homer_aggregate.done`.
metadata:
  workflow_id: epigen-atacseq_pipeline-finish
  workflow_name: epigen atacseq_pipeline finish
  step_id: homer_aggregate
  step_name: homer aggregate
---

# Scope
Use this skill only for the `homer_aggregate` step in `epigen-atacseq_pipeline-finish`.

## Orchestration
- Upstream requirements: `quantify_aggregate`
- Step file: `finish/epigen-atacseq_pipeline-finish/steps/homer_aggregate.smk`
- Config file: `finish/epigen-atacseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/homer_aggregate.done`
- Representative outputs: `results/finish/homer_aggregate.done`
- Execution targets: `homer_aggregate`
- Downstream handoff: `map_consensus_tss`

## Guardrails
- Treat `results/finish/homer_aggregate.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/homer_aggregate.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `map_consensus_tss` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/homer_aggregate.done` exists and `map_consensus_tss` can proceed without re-running homer aggregate.
