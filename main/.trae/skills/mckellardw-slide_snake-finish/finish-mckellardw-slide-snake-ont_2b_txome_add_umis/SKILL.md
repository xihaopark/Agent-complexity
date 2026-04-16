---
name: finish-mckellardw-slide-snake-ont_2b_txome_add_umis
description: Use this skill when orchestrating the retained "ont_2b_txome_add_umis" step of the mckellardw slide_snake finish finish workflow. It keeps the ont 2b txome add umis stage tied to upstream `ont_2b_txome_add_corrected_barcodes` and the downstream handoff to `ont_2b_txome_filter_bam_empty_tags`. It tracks completion via `results/finish/ont_2b_txome_add_umis.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ont_2b_txome_add_umis
  step_name: ont 2b txome add umis
---

# Scope
Use this skill only for the `ont_2b_txome_add_umis` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ont_2b_txome_add_corrected_barcodes`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ont_2b_txome_add_umis.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ont_2b_txome_add_umis.done`
- Representative outputs: `results/finish/ont_2b_txome_add_umis.done`
- Execution targets: `ont_2b_txome_add_umis`
- Downstream handoff: `ont_2b_txome_filter_bam_empty_tags`

## Guardrails
- Treat `results/finish/ont_2b_txome_add_umis.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ont_2b_txome_add_umis.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ont_2b_txome_filter_bam_empty_tags` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ont_2b_txome_add_umis.done` exists and `ont_2b_txome_filter_bam_empty_tags` can proceed without re-running ont 2b txome add umis.
