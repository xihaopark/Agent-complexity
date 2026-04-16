---
name: finish-tgirke-systempiperdata-spscrna-pca
description: Use this skill when orchestrating the retained "pca" step of the tgirke systempiperdata spscrna finish finish workflow. It keeps the pca stage tied to upstream `scaling` and the downstream handoff to `pca_plots`. It tracks completion via `results/finish/pca.done`.
metadata:
  workflow_id: tgirke-systempiperdata-spscrna-finish
  workflow_name: tgirke systempiperdata spscrna finish
  step_id: pca
  step_name: pca
---

# Scope
Use this skill only for the `pca` step in `tgirke-systempiperdata-spscrna-finish`.

## Orchestration
- Upstream requirements: `scaling`
- Step file: `finish/tgirke-systempiperdata-spscrna-finish/steps/pca.smk`
- Config file: `finish/tgirke-systempiperdata-spscrna-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/pca.done`
- Representative outputs: `results/finish/pca.done`
- Execution targets: `pca`
- Downstream handoff: `pca_plots`

## Guardrails
- Treat `results/finish/pca.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/pca.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `pca_plots` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/pca.done` exists and `pca_plots` can proceed without re-running pca.
