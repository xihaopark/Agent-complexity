---
name: finish-snakemake-workflows-microsatellite-instability-detection-with-msisensor-pro-msisensor_pro_msi
description: Use this skill when orchestrating the retained "msisensor_pro_msi" step of the snakemake workflows microsatellite instability detection with msisensor pro finish finish workflow. It keeps the msisensor pro msi stage tied to upstream `msisensor_pro_pro_run` and the downstream handoff to `merge_msi_results`. It tracks completion via `results/finish/msisensor_pro_msi.done`.
metadata:
  workflow_id: microsatellite-instability-detection-with-msisensor-pro-finish
  workflow_name: snakemake workflows microsatellite instability detection with msisensor pro finish
  step_id: msisensor_pro_msi
  step_name: msisensor pro msi
---

# Scope
Use this skill only for the `msisensor_pro_msi` step in `microsatellite-instability-detection-with-msisensor-pro-finish`.

## Orchestration
- Upstream requirements: `msisensor_pro_pro_run`
- Step file: `finish/microsatellite-instability-detection-with-msisensor-pro-finish/steps/msisensor_pro_msi.smk`
- Config file: `finish/microsatellite-instability-detection-with-msisensor-pro-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/msisensor_pro_msi.done`
- Representative outputs: `results/finish/msisensor_pro_msi.done`
- Execution targets: `msisensor_pro_msi`
- Downstream handoff: `merge_msi_results`

## Guardrails
- Treat `results/finish/msisensor_pro_msi.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/msisensor_pro_msi.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `merge_msi_results` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/msisensor_pro_msi.done` exists and `merge_msi_results` can proceed without re-running msisensor pro msi.
