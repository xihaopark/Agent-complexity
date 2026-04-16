---
name: finish-mckellardw-slide-snake-ilmn_1c_filter_barcodes
description: Use this skill when orchestrating the retained "ilmn_1c_filter_barcodes" step of the mckellardw slide_snake finish finish workflow. It keeps the ilmn 1c filter barcodes stage tied to upstream `ilmn_1c_fastq_call_bc_from_adapter` and the downstream handoff to `ilmn_1c_tsv_bc_correction`. It tracks completion via `results/finish/ilmn_1c_filter_barcodes.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ilmn_1c_filter_barcodes
  step_name: ilmn 1c filter barcodes
---

# Scope
Use this skill only for the `ilmn_1c_filter_barcodes` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ilmn_1c_fastq_call_bc_from_adapter`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ilmn_1c_filter_barcodes.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ilmn_1c_filter_barcodes.done`
- Representative outputs: `results/finish/ilmn_1c_filter_barcodes.done`
- Execution targets: `ilmn_1c_filter_barcodes`
- Downstream handoff: `ilmn_1c_tsv_bc_correction`

## Guardrails
- Treat `results/finish/ilmn_1c_filter_barcodes.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ilmn_1c_filter_barcodes.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ilmn_1c_tsv_bc_correction` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ilmn_1c_filter_barcodes.done` exists and `ilmn_1c_tsv_bc_correction` can proceed without re-running ilmn 1c filter barcodes.
