---
name: finish-epigen-spilterlize-integrate-norm_edger
description: Use this skill when orchestrating the retained "norm_edgeR" step of the epigen spilterlize_integrate finish finish workflow. It keeps the norm edgeR stage tied to upstream `select_hvf` and the downstream handoff to `norm_cqn`. It tracks completion via `results/finish/norm_edgeR.done`.
metadata:
  workflow_id: epigen-spilterlize_integrate-finish
  workflow_name: epigen spilterlize_integrate finish
  step_id: norm_edgeR
  step_name: norm edgeR
---

# Scope
Use this skill only for the `norm_edgeR` step in `epigen-spilterlize_integrate-finish`.

## Orchestration
- Upstream requirements: `select_hvf`
- Step file: `finish/epigen-spilterlize_integrate-finish/steps/norm_edgeR.smk`
- Config file: `finish/epigen-spilterlize_integrate-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/norm_edgeR.done`
- Representative outputs: `results/finish/norm_edgeR.done`
- Execution targets: `norm_edgeR`
- Downstream handoff: `norm_cqn`

## Guardrails
- Treat `results/finish/norm_edgeR.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/norm_edgeR.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `norm_cqn` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/norm_edgeR.done` exists and `norm_cqn` can proceed without re-running norm edgeR.
