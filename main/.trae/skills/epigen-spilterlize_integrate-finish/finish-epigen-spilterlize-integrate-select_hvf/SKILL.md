---
name: finish-epigen-spilterlize-integrate-select_hvf
description: Use this skill when orchestrating the retained "select_hvf" step of the epigen spilterlize_integrate finish finish workflow. It keeps the select hvf stage tied to upstream `filter_features` and the downstream handoff to `norm_edgeR`. It tracks completion via `results/finish/select_hvf.done`.
metadata:
  workflow_id: epigen-spilterlize_integrate-finish
  workflow_name: epigen spilterlize_integrate finish
  step_id: select_hvf
  step_name: select hvf
---

# Scope
Use this skill only for the `select_hvf` step in `epigen-spilterlize_integrate-finish`.

## Orchestration
- Upstream requirements: `filter_features`
- Step file: `finish/epigen-spilterlize_integrate-finish/steps/select_hvf.smk`
- Config file: `finish/epigen-spilterlize_integrate-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/select_hvf.done`
- Representative outputs: `results/finish/select_hvf.done`
- Execution targets: `select_hvf`
- Downstream handoff: `norm_edgeR`

## Guardrails
- Treat `results/finish/select_hvf.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/select_hvf.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `norm_edgeR` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/select_hvf.done` exists and `norm_edgeR` can proceed without re-running select hvf.
