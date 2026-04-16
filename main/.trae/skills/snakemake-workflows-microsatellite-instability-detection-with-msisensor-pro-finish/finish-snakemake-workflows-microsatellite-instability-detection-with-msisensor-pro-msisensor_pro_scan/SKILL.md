---
name: finish-snakemake-workflows-microsatellite-instability-detection-with-msisensor-pro-msisensor_pro_scan
description: Use this skill when orchestrating the retained "msisensor_pro_scan" step of the snakemake workflows microsatellite instability detection with msisensor pro finish finish workflow. It keeps the msisensor pro scan stage tied to upstream `download_genome` and the downstream handoff to `msisensor_pro_pro_preprocessing_baseline`. It tracks completion via `results/finish/msisensor_pro_scan.done`.
metadata:
  workflow_id: microsatellite-instability-detection-with-msisensor-pro-finish
  workflow_name: snakemake workflows microsatellite instability detection with msisensor pro finish
  step_id: msisensor_pro_scan
  step_name: msisensor pro scan
---

# Scope
Use this skill only for the `msisensor_pro_scan` step in `microsatellite-instability-detection-with-msisensor-pro-finish`.

## Orchestration
- Upstream requirements: `download_genome`
- Step file: `finish/microsatellite-instability-detection-with-msisensor-pro-finish/steps/msisensor_pro_scan.smk`
- Config file: `finish/microsatellite-instability-detection-with-msisensor-pro-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/msisensor_pro_scan.done`
- Representative outputs: `results/finish/msisensor_pro_scan.done`
- Execution targets: `msisensor_pro_scan`
- Downstream handoff: `msisensor_pro_pro_preprocessing_baseline`

## Guardrails
- Treat `results/finish/msisensor_pro_scan.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/msisensor_pro_scan.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `msisensor_pro_pro_preprocessing_baseline` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/msisensor_pro_scan.done` exists and `msisensor_pro_pro_preprocessing_baseline` can proceed without re-running msisensor pro scan.
