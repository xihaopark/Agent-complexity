---
name: finish-mckellardw-slide-snake-ont_3b_qualimap
description: Use this skill when orchestrating the retained "ont_3b_qualimap" step of the mckellardw slide_snake finish finish workflow. It keeps the ont 3b qualimap stage tied to upstream `ont_3a_readQC_compress` and the downstream handoff to `ont_3b_qualimap_readqc_summary2csv`. It tracks completion via `results/finish/ont_3b_qualimap.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ont_3b_qualimap
  step_name: ont 3b qualimap
---

# Scope
Use this skill only for the `ont_3b_qualimap` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ont_3a_readQC_compress`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ont_3b_qualimap.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ont_3b_qualimap.done`
- Representative outputs: `results/finish/ont_3b_qualimap.done`
- Execution targets: `ont_3b_qualimap`
- Downstream handoff: `ont_3b_qualimap_readqc_summary2csv`

## Guardrails
- Treat `results/finish/ont_3b_qualimap.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ont_3b_qualimap.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ont_3b_qualimap_readqc_summary2csv` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ont_3b_qualimap.done` exists and `ont_3b_qualimap_readqc_summary2csv` can proceed without re-running ont 3b qualimap.
