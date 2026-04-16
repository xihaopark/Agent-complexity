---
name: finish-epigen-unsupervised-analysis-validation_internal
description: Use this skill when orchestrating the retained "validation_internal" step of the epigen unsupervised_analysis finish finish workflow. It keeps the validation internal stage tied to upstream `validation_external` and the downstream handoff to `all`. It tracks completion via `results/finish/validation_internal.done`.
metadata:
  workflow_id: epigen-unsupervised_analysis-finish
  workflow_name: epigen unsupervised_analysis finish
  step_id: validation_internal
  step_name: validation internal
---

# Scope
Use this skill only for the `validation_internal` step in `epigen-unsupervised_analysis-finish`.

## Orchestration
- Upstream requirements: `validation_external`
- Step file: `finish/epigen-unsupervised_analysis-finish/steps/validation_internal.smk`
- Config file: `finish/epigen-unsupervised_analysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/validation_internal.done`
- Representative outputs: `results/finish/validation_internal.done`
- Execution targets: `validation_internal`
- Downstream handoff: `all`

## Guardrails
- Treat `results/finish/validation_internal.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/validation_internal.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `all` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/validation_internal.done` exists and `all` can proceed without re-running validation internal.
