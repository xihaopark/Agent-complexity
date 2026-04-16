---
name: finish-epigen-atacseq-pipeline-uropa_gencode
description: Use this skill when orchestrating the retained "uropa_gencode" step of the epigen atacseq_pipeline finish finish workflow. It keeps the uropa gencode stage tied to upstream `uropa_prepare` and the downstream handoff to `uropa_reg`. It tracks completion via `results/finish/uropa_gencode.done`.
metadata:
  workflow_id: epigen-atacseq_pipeline-finish
  workflow_name: epigen atacseq_pipeline finish
  step_id: uropa_gencode
  step_name: uropa gencode
---

# Scope
Use this skill only for the `uropa_gencode` step in `epigen-atacseq_pipeline-finish`.

## Orchestration
- Upstream requirements: `uropa_prepare`
- Step file: `finish/epigen-atacseq_pipeline-finish/steps/uropa_gencode.smk`
- Config file: `finish/epigen-atacseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/uropa_gencode.done`
- Representative outputs: `results/finish/uropa_gencode.done`
- Execution targets: `uropa_gencode`
- Downstream handoff: `uropa_reg`

## Guardrails
- Treat `results/finish/uropa_gencode.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/uropa_gencode.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `uropa_reg` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/uropa_gencode.done` exists and `uropa_reg` can proceed without re-running uropa gencode.
