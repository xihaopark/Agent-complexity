---
name: finish-epigen-spilterlize-integrate-plot_cfa
description: Use this skill when orchestrating the retained "plot_cfa" step of the epigen spilterlize_integrate finish finish workflow. It keeps the plot cfa stage tied to upstream `integrate_limma` and the downstream handoff to `plot_diagnostics`. It tracks completion via `results/finish/plot_cfa.done`.
metadata:
  workflow_id: epigen-spilterlize_integrate-finish
  workflow_name: epigen spilterlize_integrate finish
  step_id: plot_cfa
  step_name: plot cfa
---

# Scope
Use this skill only for the `plot_cfa` step in `epigen-spilterlize_integrate-finish`.

## Orchestration
- Upstream requirements: `integrate_limma`
- Step file: `finish/epigen-spilterlize_integrate-finish/steps/plot_cfa.smk`
- Config file: `finish/epigen-spilterlize_integrate-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plot_cfa.done`
- Representative outputs: `results/finish/plot_cfa.done`
- Execution targets: `plot_cfa`
- Downstream handoff: `plot_diagnostics`

## Guardrails
- Treat `results/finish/plot_cfa.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plot_cfa.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plot_diagnostics` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plot_cfa.done` exists and `plot_diagnostics` can proceed without re-running plot cfa.
