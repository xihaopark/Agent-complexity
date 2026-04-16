---
name: finish-mckellardw-slide-snake-ont_3b_qualimap_bamqc
description: Use this skill when orchestrating the retained "ont_3b_qualimap_bamqc" step of the mckellardw slide_snake finish finish workflow. It keeps the ont 3b qualimap bamqc stage tied to upstream `ont_3b_qualimap_readqc_summary2csv` and the downstream handoff to `ont_3b_qualimap_bamqc_summary2csv`. It tracks completion via `results/finish/ont_3b_qualimap_bamqc.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ont_3b_qualimap_bamqc
  step_name: ont 3b qualimap bamqc
---

# Scope
Use this skill only for the `ont_3b_qualimap_bamqc` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ont_3b_qualimap_readqc_summary2csv`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ont_3b_qualimap_bamqc.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ont_3b_qualimap_bamqc.done`
- Representative outputs: `results/finish/ont_3b_qualimap_bamqc.done`
- Execution targets: `ont_3b_qualimap_bamqc`
- Downstream handoff: `ont_3b_qualimap_bamqc_summary2csv`

## Guardrails
- Treat `results/finish/ont_3b_qualimap_bamqc.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ont_3b_qualimap_bamqc.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ont_3b_qualimap_bamqc_summary2csv` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ont_3b_qualimap_bamqc.done` exists and `ont_3b_qualimap_bamqc_summary2csv` can proceed without re-running ont 3b qualimap bamqc.
