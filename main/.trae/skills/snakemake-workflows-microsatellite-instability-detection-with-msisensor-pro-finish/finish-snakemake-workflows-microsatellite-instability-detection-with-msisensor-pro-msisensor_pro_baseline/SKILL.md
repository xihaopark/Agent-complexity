---
name: finish-snakemake-workflows-microsatellite-instability-detection-with-msisensor-pro-msisensor_pro_baseline
description: Use this skill when orchestrating the retained "msisensor_pro_baseline" step of the snakemake workflows microsatellite instability detection with msisensor pro finish finish workflow. It keeps the msisensor pro baseline stage tied to upstream `create_panel_of_normals_samples_list` and the downstream handoff to `msisensor_pro_pro_run`. It tracks completion via `results/finish/msisensor_pro_baseline.done`.
metadata:
  workflow_id: microsatellite-instability-detection-with-msisensor-pro-finish
  workflow_name: snakemake workflows microsatellite instability detection with msisensor pro finish
  step_id: msisensor_pro_baseline
  step_name: msisensor pro baseline
---

# Scope
Use this skill only for the `msisensor_pro_baseline` step in `microsatellite-instability-detection-with-msisensor-pro-finish`.

## Orchestration
- Upstream requirements: `create_panel_of_normals_samples_list`
- Step file: `finish/microsatellite-instability-detection-with-msisensor-pro-finish/steps/msisensor_pro_baseline.smk`
- Config file: `finish/microsatellite-instability-detection-with-msisensor-pro-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/msisensor_pro_baseline.done`
- Representative outputs: `results/finish/msisensor_pro_baseline.done`
- Execution targets: `msisensor_pro_baseline`
- Downstream handoff: `msisensor_pro_pro_run`

## Guardrails
- Treat `results/finish/msisensor_pro_baseline.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/msisensor_pro_baseline.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `msisensor_pro_pro_run` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/msisensor_pro_baseline.done` exists and `msisensor_pro_pro_run` can proceed without re-running msisensor pro baseline.
