---
name: finish-snakemake-workflows-microsatellite-instability-detection-with-msisensor-pro-msisensor_pro_pro_run
description: Use this skill when orchestrating the retained "msisensor_pro_pro_run" step of the snakemake workflows microsatellite instability detection with msisensor pro finish finish workflow. It keeps the msisensor pro pro run stage tied to upstream `msisensor_pro_baseline` and the downstream handoff to `msisensor_pro_msi`. It tracks completion via `results/finish/msisensor_pro_pro_run.done`.
metadata:
  workflow_id: microsatellite-instability-detection-with-msisensor-pro-finish
  workflow_name: snakemake workflows microsatellite instability detection with msisensor pro finish
  step_id: msisensor_pro_pro_run
  step_name: msisensor pro pro run
---

# Scope
Use this skill only for the `msisensor_pro_pro_run` step in `microsatellite-instability-detection-with-msisensor-pro-finish`.

## Orchestration
- Upstream requirements: `msisensor_pro_baseline`
- Step file: `finish/microsatellite-instability-detection-with-msisensor-pro-finish/steps/msisensor_pro_pro_run.smk`
- Config file: `finish/microsatellite-instability-detection-with-msisensor-pro-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/msisensor_pro_pro_run.done`
- Representative outputs: `results/finish/msisensor_pro_pro_run.done`
- Execution targets: `msisensor_pro_pro_run`
- Downstream handoff: `msisensor_pro_msi`

## Guardrails
- Treat `results/finish/msisensor_pro_pro_run.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/msisensor_pro_pro_run.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `msisensor_pro_msi` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/msisensor_pro_pro_run.done` exists and `msisensor_pro_msi` can proceed without re-running msisensor pro pro run.
