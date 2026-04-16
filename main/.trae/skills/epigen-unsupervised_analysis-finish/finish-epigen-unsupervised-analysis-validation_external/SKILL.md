---
name: finish-epigen-unsupervised-analysis-validation_external
description: Use this skill when orchestrating the retained "validation_external" step of the epigen unsupervised_analysis finish finish workflow. It keeps the validation external stage tied to upstream `umap_graph` and the downstream handoff to `validation_internal`. It tracks completion via `results/finish/validation_external.done`.
metadata:
  workflow_id: epigen-unsupervised_analysis-finish
  workflow_name: epigen unsupervised_analysis finish
  step_id: validation_external
  step_name: validation external
---

# Scope
Use this skill only for the `validation_external` step in `epigen-unsupervised_analysis-finish`.

## Orchestration
- Upstream requirements: `umap_graph`
- Step file: `finish/epigen-unsupervised_analysis-finish/steps/validation_external.smk`
- Config file: `finish/epigen-unsupervised_analysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/validation_external.done`
- Representative outputs: `results/finish/validation_external.done`
- Execution targets: `validation_external`
- Downstream handoff: `validation_internal`

## Guardrails
- Treat `results/finish/validation_external.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/validation_external.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `validation_internal` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/validation_external.done` exists and `validation_internal` can proceed without re-running validation external.
