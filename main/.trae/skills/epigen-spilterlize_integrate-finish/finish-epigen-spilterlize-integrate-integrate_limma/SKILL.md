---
name: finish-epigen-spilterlize-integrate-integrate_limma
description: Use this skill when orchestrating the retained "integrate_limma" step of the epigen spilterlize_integrate finish finish workflow. It keeps the integrate limma stage tied to upstream `norm_voom` and the downstream handoff to `plot_cfa`. It tracks completion via `results/finish/integrate_limma.done`.
metadata:
  workflow_id: epigen-spilterlize_integrate-finish
  workflow_name: epigen spilterlize_integrate finish
  step_id: integrate_limma
  step_name: integrate limma
---

# Scope
Use this skill only for the `integrate_limma` step in `epigen-spilterlize_integrate-finish`.

## Orchestration
- Upstream requirements: `norm_voom`
- Step file: `finish/epigen-spilterlize_integrate-finish/steps/integrate_limma.smk`
- Config file: `finish/epigen-spilterlize_integrate-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/integrate_limma.done`
- Representative outputs: `results/finish/integrate_limma.done`
- Execution targets: `integrate_limma`
- Downstream handoff: `plot_cfa`

## Guardrails
- Treat `results/finish/integrate_limma.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/integrate_limma.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plot_cfa` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/integrate_limma.done` exists and `plot_cfa` can proceed without re-running integrate limma.
