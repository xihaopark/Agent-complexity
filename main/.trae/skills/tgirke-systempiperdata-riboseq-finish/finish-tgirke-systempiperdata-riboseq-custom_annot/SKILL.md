---
name: finish-tgirke-systempiperdata-riboseq-custom_annot
description: Use this skill when orchestrating the retained "custom_annot" step of the tgirke systempiperdata riboseq finish finish workflow. It keeps the custom annot stage tied to upstream `run_edgeR` and the downstream handoff to `filter_degs`. It tracks completion via `results/finish/custom_annot.done`.
metadata:
  workflow_id: tgirke-systempiperdata-riboseq-finish
  workflow_name: tgirke systempiperdata riboseq finish
  step_id: custom_annot
  step_name: custom annot
---

# Scope
Use this skill only for the `custom_annot` step in `tgirke-systempiperdata-riboseq-finish`.

## Orchestration
- Upstream requirements: `run_edgeR`
- Step file: `finish/tgirke-systempiperdata-riboseq-finish/steps/custom_annot.smk`
- Config file: `finish/tgirke-systempiperdata-riboseq-finish/config_basic/config.yaml`
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
