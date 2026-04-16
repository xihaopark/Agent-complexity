---
name: finish-epigen-spilterlize-integrate-filter_features
description: Use this skill when orchestrating the retained "filter_features" step of the epigen spilterlize_integrate finish finish workflow. It keeps the filter features stage tied to upstream `split` and the downstream handoff to `select_hvf`. It tracks completion via `results/finish/filter_features.done`.
metadata:
  workflow_id: epigen-spilterlize_integrate-finish
  workflow_name: epigen spilterlize_integrate finish
  step_id: filter_features
  step_name: filter features
---

# Scope
Use this skill only for the `filter_features` step in `epigen-spilterlize_integrate-finish`.

## Orchestration
- Upstream requirements: `split`
- Step file: `finish/epigen-spilterlize_integrate-finish/steps/filter_features.smk`
- Config file: `finish/epigen-spilterlize_integrate-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/filter_features.done`
- Representative outputs: `results/finish/filter_features.done`
- Execution targets: `filter_features`
- Downstream handoff: `select_hvf`

## Guardrails
- Treat `results/finish/filter_features.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/filter_features.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `select_hvf` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/filter_features.done` exists and `select_hvf` can proceed without re-running filter features.
