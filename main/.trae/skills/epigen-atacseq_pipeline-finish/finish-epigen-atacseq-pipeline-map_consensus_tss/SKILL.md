---
name: finish-epigen-atacseq-pipeline-map_consensus_tss
description: Use this skill when orchestrating the retained "map_consensus_tss" step of the epigen atacseq_pipeline finish finish workflow. It keeps the map consensus tss stage tied to upstream `homer_aggregate` and the downstream handoff to `uropa_prepare`. It tracks completion via `results/finish/map_consensus_tss.done`.
metadata:
  workflow_id: epigen-atacseq_pipeline-finish
  workflow_name: epigen atacseq_pipeline finish
  step_id: map_consensus_tss
  step_name: map consensus tss
---

# Scope
Use this skill only for the `map_consensus_tss` step in `epigen-atacseq_pipeline-finish`.

## Orchestration
- Upstream requirements: `homer_aggregate`
- Step file: `finish/epigen-atacseq_pipeline-finish/steps/map_consensus_tss.smk`
- Config file: `finish/epigen-atacseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/map_consensus_tss.done`
- Representative outputs: `results/finish/map_consensus_tss.done`
- Execution targets: `map_consensus_tss`
- Downstream handoff: `uropa_prepare`

## Guardrails
- Treat `results/finish/map_consensus_tss.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/map_consensus_tss.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `uropa_prepare` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/map_consensus_tss.done` exists and `uropa_prepare` can proceed without re-running map consensus tss.
