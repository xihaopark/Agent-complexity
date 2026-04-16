---
name: finish-epigen-atacseq-pipeline-uropa_prepare
description: Use this skill when orchestrating the retained "uropa_prepare" step of the epigen atacseq_pipeline finish finish workflow. It keeps the uropa prepare stage tied to upstream `map_consensus_tss` and the downstream handoff to `uropa_gencode`. It tracks completion via `results/finish/uropa_prepare.done`.
metadata:
  workflow_id: epigen-atacseq_pipeline-finish
  workflow_name: epigen atacseq_pipeline finish
  step_id: uropa_prepare
  step_name: uropa prepare
---

# Scope
Use this skill only for the `uropa_prepare` step in `epigen-atacseq_pipeline-finish`.

## Orchestration
- Upstream requirements: `map_consensus_tss`
- Step file: `finish/epigen-atacseq_pipeline-finish/steps/uropa_prepare.smk`
- Config file: `finish/epigen-atacseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/uropa_prepare.done`
- Representative outputs: `results/finish/uropa_prepare.done`
- Execution targets: `uropa_prepare`
- Downstream handoff: `uropa_gencode`

## Guardrails
- Treat `results/finish/uropa_prepare.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/uropa_prepare.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `uropa_gencode` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/uropa_prepare.done` exists and `uropa_gencode` can proceed without re-running uropa prepare.
