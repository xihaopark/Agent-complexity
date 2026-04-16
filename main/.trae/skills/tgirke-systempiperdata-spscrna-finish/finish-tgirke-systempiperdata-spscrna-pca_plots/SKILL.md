---
name: finish-tgirke-systempiperdata-spscrna-pca_plots
description: Use this skill when orchestrating the retained "pca_plots" step of the tgirke systempiperdata spscrna finish finish workflow. It keeps the pca plots stage tied to upstream `pca` and the downstream handoff to `choose_pcs`. It tracks completion via `results/finish/pca_plots.done`.
metadata:
  workflow_id: tgirke-systempiperdata-spscrna-finish
  workflow_name: tgirke systempiperdata spscrna finish
  step_id: pca_plots
  step_name: pca plots
---

# Scope
Use this skill only for the `pca_plots` step in `tgirke-systempiperdata-spscrna-finish`.

## Orchestration
- Upstream requirements: `pca`
- Step file: `finish/tgirke-systempiperdata-spscrna-finish/steps/pca_plots.smk`
- Config file: `finish/tgirke-systempiperdata-spscrna-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/pca_plots.done`
- Representative outputs: `results/finish/pca_plots.done`
- Execution targets: `pca_plots`
- Downstream handoff: `choose_pcs`

## Guardrails
- Treat `results/finish/pca_plots.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/pca_plots.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `choose_pcs` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/pca_plots.done` exists and `choose_pcs` can proceed without re-running pca plots.
