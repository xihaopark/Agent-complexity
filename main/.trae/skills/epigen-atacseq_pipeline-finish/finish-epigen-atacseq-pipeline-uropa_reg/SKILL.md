---
name: finish-epigen-atacseq-pipeline-uropa_reg
description: Use this skill when orchestrating the retained "uropa_reg" step of the epigen atacseq_pipeline finish finish workflow. It keeps the uropa reg stage tied to upstream `uropa_gencode` and the downstream handoff to `homer_region_annotation`. It tracks completion via `results/finish/uropa_reg.done`.
metadata:
  workflow_id: epigen-atacseq_pipeline-finish
  workflow_name: epigen atacseq_pipeline finish
  step_id: uropa_reg
  step_name: uropa reg
---

# Scope
Use this skill only for the `uropa_reg` step in `epigen-atacseq_pipeline-finish`.

## Orchestration
- Upstream requirements: `uropa_gencode`
- Step file: `finish/epigen-atacseq_pipeline-finish/steps/uropa_reg.smk`
- Config file: `finish/epigen-atacseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/uropa_reg.done`
- Representative outputs: `results/finish/uropa_reg.done`
- Execution targets: `uropa_reg`
- Downstream handoff: `homer_region_annotation`

## Guardrails
- Treat `results/finish/uropa_reg.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/uropa_reg.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `homer_region_annotation` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/uropa_reg.done` exists and `homer_region_annotation` can proceed without re-running uropa reg.
