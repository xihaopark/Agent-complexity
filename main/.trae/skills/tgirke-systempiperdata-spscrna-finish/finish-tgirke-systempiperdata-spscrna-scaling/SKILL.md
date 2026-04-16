---
name: finish-tgirke-systempiperdata-spscrna-scaling
description: Use this skill when orchestrating the retained "scaling" step of the tgirke systempiperdata spscrna finish finish workflow. It keeps the scaling stage tied to upstream `find_var_genes` and the downstream handoff to `pca`. It tracks completion via `results/finish/scaling.done`.
metadata:
  workflow_id: tgirke-systempiperdata-spscrna-finish
  workflow_name: tgirke systempiperdata spscrna finish
  step_id: scaling
  step_name: scaling
---

# Scope
Use this skill only for the `scaling` step in `tgirke-systempiperdata-spscrna-finish`.

## Orchestration
- Upstream requirements: `find_var_genes`
- Step file: `finish/tgirke-systempiperdata-spscrna-finish/steps/scaling.smk`
- Config file: `finish/tgirke-systempiperdata-spscrna-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/scaling.done`
- Representative outputs: `results/finish/scaling.done`
- Execution targets: `scaling`
- Downstream handoff: `pca`

## Guardrails
- Treat `results/finish/scaling.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/scaling.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `pca` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/scaling.done` exists and `pca` can proceed without re-running scaling.
