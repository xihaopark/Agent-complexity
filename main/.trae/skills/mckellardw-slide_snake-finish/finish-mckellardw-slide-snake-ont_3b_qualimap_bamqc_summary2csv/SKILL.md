---
name: finish-mckellardw-slide-snake-ont_3b_qualimap_bamqc_summary2csv
description: Use this skill when orchestrating the retained "ont_3b_qualimap_bamqc_summary2csv" step of the mckellardw slide_snake finish finish workflow. It keeps the ont 3b qualimap bamqc summary2csv stage tied to upstream `ont_3b_qualimap_bamqc` and the downstream handoff to `all`. It tracks completion via `results/finish/ont_3b_qualimap_bamqc_summary2csv.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ont_3b_qualimap_bamqc_summary2csv
  step_name: ont 3b qualimap bamqc summary2csv
---

# Scope
Use this skill only for the `ont_3b_qualimap_bamqc_summary2csv` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ont_3b_qualimap_bamqc`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ont_3b_qualimap_bamqc_summary2csv.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ont_3b_qualimap_bamqc_summary2csv.done`
- Representative outputs: `results/finish/ont_3b_qualimap_bamqc_summary2csv.done`
- Execution targets: `ont_3b_qualimap_bamqc_summary2csv`
- Downstream handoff: `all`

## Guardrails
- Treat `results/finish/ont_3b_qualimap_bamqc_summary2csv.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ont_3b_qualimap_bamqc_summary2csv.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `all` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ont_3b_qualimap_bamqc_summary2csv.done` exists and `all` can proceed without re-running ont 3b qualimap bamqc summary2csv.
