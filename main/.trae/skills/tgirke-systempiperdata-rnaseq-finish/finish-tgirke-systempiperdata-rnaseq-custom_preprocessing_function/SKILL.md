---
name: finish-tgirke-systempiperdata-rnaseq-custom_preprocessing_function
description: Use this skill when orchestrating the retained "custom_preprocessing_function" step of the tgirke systempiperdata rnaseq finish finish workflow. It keeps the custom preprocessing function stage tied to upstream `preprocessing` and the downstream handoff to `trimming`. It tracks completion via `results/finish/custom_preprocessing_function.done`.
metadata:
  workflow_id: tgirke-systempiperdata-rnaseq-finish
  workflow_name: tgirke systempiperdata rnaseq finish
  step_id: custom_preprocessing_function
  step_name: custom preprocessing function
---

# Scope
Use this skill only for the `custom_preprocessing_function` step in `tgirke-systempiperdata-rnaseq-finish`.

## Orchestration
- Upstream requirements: `preprocessing`
- Step file: `finish/tgirke-systempiperdata-rnaseq-finish/steps/custom_preprocessing_function.smk`
- Config file: `finish/tgirke-systempiperdata-rnaseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/custom_preprocessing_function.done`
- Representative outputs: `results/finish/custom_preprocessing_function.done`
- Execution targets: `custom_preprocessing_function`
- Downstream handoff: `trimming`

## Guardrails
- Treat `results/finish/custom_preprocessing_function.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/custom_preprocessing_function.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `trimming` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/custom_preprocessing_function.done` exists and `trimming` can proceed without re-running custom preprocessing function.
