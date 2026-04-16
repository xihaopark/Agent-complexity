---
name: finish-mckellardw-slide-snake-ont_1c_filter_barcodes
description: Use this skill when orchestrating the retained "ont_1c_filter_barcodes" step of the mckellardw slide_snake finish finish workflow. It keeps the ont 1c filter barcodes stage tied to upstream `ont_1c_fastq_call_bc_from_adapter` and the downstream handoff to `ont_1c_tsv_bc_correction`. It tracks completion via `results/finish/ont_1c_filter_barcodes.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ont_1c_filter_barcodes
  step_name: ont 1c filter barcodes
---

# Scope
Use this skill only for the `ont_1c_filter_barcodes` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ont_1c_fastq_call_bc_from_adapter`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ont_1c_filter_barcodes.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ont_1c_filter_barcodes.done`
- Representative outputs: `results/finish/ont_1c_filter_barcodes.done`
- Execution targets: `ont_1c_filter_barcodes`
- Downstream handoff: `ont_1c_tsv_bc_correction`

## Guardrails
- Treat `results/finish/ont_1c_filter_barcodes.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ont_1c_filter_barcodes.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ont_1c_tsv_bc_correction` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ont_1c_filter_barcodes.done` exists and `ont_1c_tsv_bc_correction` can proceed without re-running ont 1c filter barcodes.
