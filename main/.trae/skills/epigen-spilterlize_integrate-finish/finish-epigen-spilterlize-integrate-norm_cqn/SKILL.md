---
name: finish-epigen-spilterlize-integrate-norm_cqn
description: Use this skill when orchestrating the retained "norm_cqn" step of the epigen spilterlize_integrate finish finish workflow. It keeps the norm cqn stage tied to upstream `norm_edgeR` and the downstream handoff to `norm_voom`. It tracks completion via `results/finish/norm_cqn.done`.
metadata:
  workflow_id: epigen-spilterlize_integrate-finish
  workflow_name: epigen spilterlize_integrate finish
  step_id: norm_cqn
  step_name: norm cqn
---

# Scope
Use this skill only for the `norm_cqn` step in `epigen-spilterlize_integrate-finish`.

## Orchestration
- Upstream requirements: `norm_edgeR`
- Step file: `finish/epigen-spilterlize_integrate-finish/steps/norm_cqn.smk`
- Config file: `finish/epigen-spilterlize_integrate-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/norm_cqn.done`
- Representative outputs: `results/finish/norm_cqn.done`
- Execution targets: `norm_cqn`
- Downstream handoff: `norm_voom`

## Guardrails
- Treat `results/finish/norm_cqn.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/norm_cqn.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `norm_voom` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/norm_cqn.done` exists and `norm_voom` can proceed without re-running norm cqn.
