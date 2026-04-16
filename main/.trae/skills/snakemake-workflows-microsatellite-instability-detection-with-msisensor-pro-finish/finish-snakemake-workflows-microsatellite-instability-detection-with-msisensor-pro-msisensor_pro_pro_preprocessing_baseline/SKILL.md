---
name: finish-snakemake-workflows-microsatellite-instability-detection-with-msisensor-pro-msisensor_pro_pro_preprocessing_baseline
description: Use this skill when orchestrating the retained "msisensor_pro_pro_preprocessing_baseline" step of the snakemake workflows microsatellite instability detection with msisensor pro finish finish workflow. It keeps the msisensor pro pro preprocessing baseline stage tied to upstream `msisensor_pro_scan` and the downstream handoff to `create_panel_of_normals_samples_list`. It tracks completion via `results/finish/msisensor_pro_pro_preprocessing_baseline.done`.
metadata:
  workflow_id: microsatellite-instability-detection-with-msisensor-pro-finish
  workflow_name: snakemake workflows microsatellite instability detection with msisensor pro finish
  step_id: msisensor_pro_pro_preprocessing_baseline
  step_name: msisensor pro pro preprocessing baseline
---

# Scope
Use this skill only for the `msisensor_pro_pro_preprocessing_baseline` step in `microsatellite-instability-detection-with-msisensor-pro-finish`.

## Orchestration
- Upstream requirements: `msisensor_pro_scan`
- Step file: `finish/microsatellite-instability-detection-with-msisensor-pro-finish/steps/msisensor_pro_pro_preprocessing_baseline.smk`
- Config file: `finish/microsatellite-instability-detection-with-msisensor-pro-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/msisensor_pro_pro_preprocessing_baseline.done`
- Representative outputs: `results/finish/msisensor_pro_pro_preprocessing_baseline.done`
- Execution targets: `msisensor_pro_pro_preprocessing_baseline`
- Downstream handoff: `create_panel_of_normals_samples_list`

## Guardrails
- Treat `results/finish/msisensor_pro_pro_preprocessing_baseline.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/msisensor_pro_pro_preprocessing_baseline.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `create_panel_of_normals_samples_list` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/msisensor_pro_pro_preprocessing_baseline.done` exists and `create_panel_of_normals_samples_list` can proceed without re-running msisensor pro pro preprocessing baseline.
