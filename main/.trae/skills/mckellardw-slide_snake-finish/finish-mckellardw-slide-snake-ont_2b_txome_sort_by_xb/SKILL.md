---
name: finish-mckellardw-slide-snake-ont_2b_txome_sort_by_xb
description: Use this skill when orchestrating the retained "ont_2b_txome_sort_by_xb" step of the mckellardw slide_snake finish finish workflow. It keeps the ont 2b txome sort by xb stage tied to upstream `ont_2b_txome_dedup_by_xb` and the downstream handoff to `ont_2b_txome_oarfish_quant`. It tracks completion via `results/finish/ont_2b_txome_sort_by_xb.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ont_2b_txome_sort_by_xb
  step_name: ont 2b txome sort by xb
---

# Scope
Use this skill only for the `ont_2b_txome_sort_by_xb` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ont_2b_txome_dedup_by_xb`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ont_2b_txome_sort_by_xb.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ont_2b_txome_sort_by_xb.done`
- Representative outputs: `results/finish/ont_2b_txome_sort_by_xb.done`
- Execution targets: `ont_2b_txome_sort_by_xb`
- Downstream handoff: `ont_2b_txome_oarfish_quant`

## Guardrails
- Treat `results/finish/ont_2b_txome_sort_by_xb.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ont_2b_txome_sort_by_xb.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ont_2b_txome_oarfish_quant` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ont_2b_txome_sort_by_xb.done` exists and `ont_2b_txome_oarfish_quant` can proceed without re-running ont 2b txome sort by xb.
