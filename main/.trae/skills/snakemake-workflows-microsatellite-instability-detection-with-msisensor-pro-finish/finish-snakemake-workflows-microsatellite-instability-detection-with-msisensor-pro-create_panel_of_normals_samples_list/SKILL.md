---
name: finish-snakemake-workflows-microsatellite-instability-detection-with-msisensor-pro-create_panel_of_normals_samples_list
description: Use this skill when orchestrating the retained "create_panel_of_normals_samples_list" step of the snakemake workflows microsatellite instability detection with msisensor pro finish finish workflow. It keeps the create panel of normals samples list stage tied to upstream `msisensor_pro_pro_preprocessing_baseline` and the downstream handoff to `msisensor_pro_baseline`. It tracks completion via `results/finish/create_panel_of_normals_samples_list.done`.
metadata:
  workflow_id: microsatellite-instability-detection-with-msisensor-pro-finish
  workflow_name: snakemake workflows microsatellite instability detection with msisensor pro finish
  step_id: create_panel_of_normals_samples_list
  step_name: create panel of normals samples list
---

# Scope
Use this skill only for the `create_panel_of_normals_samples_list` step in `microsatellite-instability-detection-with-msisensor-pro-finish`.

## Orchestration
- Upstream requirements: `msisensor_pro_pro_preprocessing_baseline`
- Step file: `finish/microsatellite-instability-detection-with-msisensor-pro-finish/steps/create_panel_of_normals_samples_list.smk`
- Config file: `finish/microsatellite-instability-detection-with-msisensor-pro-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/create_panel_of_normals_samples_list.done`
- Representative outputs: `results/finish/create_panel_of_normals_samples_list.done`
- Execution targets: `create_panel_of_normals_samples_list`
- Downstream handoff: `msisensor_pro_baseline`

## Guardrails
- Treat `results/finish/create_panel_of_normals_samples_list.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/create_panel_of_normals_samples_list.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `msisensor_pro_baseline` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/create_panel_of_normals_samples_list.done` exists and `msisensor_pro_baseline` can proceed without re-running create panel of normals samples list.
