---
name: finish-mckellardw-slide-snake-ilmn_3u_filter_nogn
description: Use this skill when orchestrating the retained "ilmn_3u_filter_noGN" step of the mckellardw slide_snake finish finish workflow. It keeps the ilmn 3u filter noGN stage tied to upstream `ilmn_3q_qualimap_bamqc_summary2csv_STAR` and the downstream handoff to `ilmn_3u_calcHMMbed`. It tracks completion via `results/finish/ilmn_3u_filter_noGN.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ilmn_3u_filter_noGN
  step_name: ilmn 3u filter noGN
---

# Scope
Use this skill only for the `ilmn_3u_filter_noGN` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ilmn_3q_qualimap_bamqc_summary2csv_STAR`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ilmn_3u_filter_noGN.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ilmn_3u_filter_noGN.done`
- Representative outputs: `results/finish/ilmn_3u_filter_noGN.done`
- Execution targets: `ilmn_3u_filter_noGN`
- Downstream handoff: `ilmn_3u_calcHMMbed`

## Guardrails
- Treat `results/finish/ilmn_3u_filter_noGN.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ilmn_3u_filter_noGN.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ilmn_3u_calcHMMbed` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ilmn_3u_filter_noGN.done` exists and `ilmn_3u_calcHMMbed` can proceed without re-running ilmn 3u filter noGN.
