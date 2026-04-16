---
name: finish-tgirke-systempiperdata-rnaseq-custom_annot
description: Use this skill when orchestrating the retained "custom_annot" step of the tgirke systempiperdata rnaseq finish finish workflow. It keeps the custom annot stage tied to upstream `run_edger` and the downstream handoff to `filter_degs`. It tracks completion via `results/finish/custom_annot.done`.
metadata:
  workflow_id: tgirke-systempiperdata-rnaseq-finish
  workflow_name: tgirke systempiperdata rnaseq finish
  step_id: custom_annot
  step_name: custom annot
---

# Scope
Use this skill only for the `custom_annot` step in `tgirke-systempiperdata-rnaseq-finish`.

## Orchestration
- Upstream requirements: `run_edger`
- Step file: `finish/tgirke-systempiperdata-rnaseq-finish/steps/custom_annot.smk`
- Config file: `finish/tgirke-systempiperdata-rnaseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/custom_annot.done`
- Representative outputs: `results/finish/custom_annot.done`
- Execution targets: `custom_annot`
- Downstream handoff: `filter_degs`

## Guardrails
- Treat `results/finish/custom_annot.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/custom_annot.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `filter_degs` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/custom_annot.done` exists and `filter_degs` can proceed without re-running custom annot.
