---
name: finish-snakemake-workflows-microsatellite-instability-detection-with-msisensor-pro-merge_msi_results
description: Use this skill when orchestrating the retained "merge_msi_results" step of the snakemake workflows microsatellite instability detection with msisensor pro finish finish workflow. It keeps the merge msi results stage tied to upstream `msisensor_pro_msi` and the downstream handoff to `all`. It tracks completion via `results/finish/merge_msi_results.done`.
metadata:
  workflow_id: microsatellite-instability-detection-with-msisensor-pro-finish
  workflow_name: snakemake workflows microsatellite instability detection with msisensor pro finish
  step_id: merge_msi_results
  step_name: merge msi results
---

# Scope
Use this skill only for the `merge_msi_results` step in `microsatellite-instability-detection-with-msisensor-pro-finish`.

## Orchestration
- Upstream requirements: `msisensor_pro_msi`
- Step file: `finish/microsatellite-instability-detection-with-msisensor-pro-finish/steps/merge_msi_results.smk`
- Config file: `finish/microsatellite-instability-detection-with-msisensor-pro-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/merge_msi_results.done`
- Representative outputs: `results/finish/merge_msi_results.done`
- Execution targets: `merge_msi_results`
- Downstream handoff: `all`

## Guardrails
- Treat `results/finish/merge_msi_results.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/merge_msi_results.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `all` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/merge_msi_results.done` exists and `all` can proceed without re-running merge msi results.
