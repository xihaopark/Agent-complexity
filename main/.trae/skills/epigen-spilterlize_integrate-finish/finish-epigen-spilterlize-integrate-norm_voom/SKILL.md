---
name: finish-epigen-spilterlize-integrate-norm_voom
description: Use this skill when orchestrating the retained "norm_voom" step of the epigen spilterlize_integrate finish finish workflow. It keeps the norm voom stage tied to upstream `norm_cqn` and the downstream handoff to `integrate_limma`. It tracks completion via `results/finish/norm_voom.done`.
metadata:
  workflow_id: epigen-spilterlize_integrate-finish
  workflow_name: epigen spilterlize_integrate finish
  step_id: norm_voom
  step_name: norm voom
---

# Scope
Use this skill only for the `norm_voom` step in `epigen-spilterlize_integrate-finish`.

## Orchestration
- Upstream requirements: `norm_cqn`
- Step file: `finish/epigen-spilterlize_integrate-finish/steps/norm_voom.smk`
- Config file: `finish/epigen-spilterlize_integrate-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/norm_voom.done`
- Representative outputs: `results/finish/norm_voom.done`
- Execution targets: `norm_voom`
- Downstream handoff: `integrate_limma`

## Guardrails
- Treat `results/finish/norm_voom.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/norm_voom.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `integrate_limma` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/norm_voom.done` exists and `integrate_limma` can proceed without re-running norm voom.
