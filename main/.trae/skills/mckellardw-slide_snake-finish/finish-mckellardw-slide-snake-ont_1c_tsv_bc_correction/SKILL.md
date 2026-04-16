---
name: finish-mckellardw-slide-snake-ont_1c_tsv_bc_correction
description: Use this skill when orchestrating the retained "ont_1c_tsv_bc_correction" step of the mckellardw slide_snake finish finish workflow. It keeps the ont 1c tsv bc correction stage tied to upstream `ont_1c_filter_barcodes` and the downstream handoff to `ont_1c_summarize_bc_correction`. It tracks completion via `results/finish/ont_1c_tsv_bc_correction.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ont_1c_tsv_bc_correction
  step_name: ont 1c tsv bc correction
---

# Scope
Use this skill only for the `ont_1c_tsv_bc_correction` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ont_1c_filter_barcodes`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ont_1c_tsv_bc_correction.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ont_1c_tsv_bc_correction.done`
- Representative outputs: `results/finish/ont_1c_tsv_bc_correction.done`
- Execution targets: `ont_1c_tsv_bc_correction`
- Downstream handoff: `ont_1c_summarize_bc_correction`

## Guardrails
- Treat `results/finish/ont_1c_tsv_bc_correction.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ont_1c_tsv_bc_correction.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ont_1c_summarize_bc_correction` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ont_1c_tsv_bc_correction.done` exists and `ont_1c_summarize_bc_correction` can proceed without re-running ont 1c tsv bc correction.
