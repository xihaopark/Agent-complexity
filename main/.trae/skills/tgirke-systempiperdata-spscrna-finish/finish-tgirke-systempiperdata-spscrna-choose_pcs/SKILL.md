---
name: finish-tgirke-systempiperdata-spscrna-choose_pcs
description: Use this skill when orchestrating the retained "choose_pcs" step of the tgirke systempiperdata spscrna finish finish workflow. It keeps the choose pcs stage tied to upstream `pca_plots` and the downstream handoff to `find_clusters`. It tracks completion via `results/finish/choose_pcs.done`.
metadata:
  workflow_id: tgirke-systempiperdata-spscrna-finish
  workflow_name: tgirke systempiperdata spscrna finish
  step_id: choose_pcs
  step_name: choose pcs
---

# Scope
Use this skill only for the `choose_pcs` step in `tgirke-systempiperdata-spscrna-finish`.

## Orchestration
- Upstream requirements: `pca_plots`
- Step file: `finish/tgirke-systempiperdata-spscrna-finish/steps/choose_pcs.smk`
- Config file: `finish/tgirke-systempiperdata-spscrna-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/choose_pcs.done`
- Representative outputs: `results/finish/choose_pcs.done`
- Execution targets: `choose_pcs`
- Downstream handoff: `find_clusters`

## Guardrails
- Treat `results/finish/choose_pcs.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/choose_pcs.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `find_clusters` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/choose_pcs.done` exists and `find_clusters` can proceed without re-running choose pcs.
