---
name: finish-mckellardw-slide-snake-ont_2b_txome_oarfish_quant
description: Use this skill when orchestrating the retained "ont_2b_txome_oarfish_quant" step of the mckellardw slide_snake finish finish workflow. It keeps the ont 2b txome oarfish quant stage tied to upstream `ont_2b_txome_sort_by_xb` and the downstream handoff to `ont_2b_txome_compress_oarfish_matrix`. It tracks completion via `results/finish/ont_2b_txome_oarfish_quant.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ont_2b_txome_oarfish_quant
  step_name: ont 2b txome oarfish quant
---

# Scope
Use this skill only for the `ont_2b_txome_oarfish_quant` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ont_2b_txome_sort_by_xb`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ont_2b_txome_oarfish_quant.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ont_2b_txome_oarfish_quant.done`
- Representative outputs: `results/finish/ont_2b_txome_oarfish_quant.done`
- Execution targets: `ont_2b_txome_oarfish_quant`
- Downstream handoff: `ont_2b_txome_compress_oarfish_matrix`

## Guardrails
- Treat `results/finish/ont_2b_txome_oarfish_quant.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ont_2b_txome_oarfish_quant.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ont_2b_txome_compress_oarfish_matrix` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ont_2b_txome_oarfish_quant.done` exists and `ont_2b_txome_compress_oarfish_matrix` can proceed without re-running ont 2b txome oarfish quant.
