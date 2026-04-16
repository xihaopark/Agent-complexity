---
name: finish-mckellardw-slide-snake-ilmn_3u_filter_out_atars
description: Use this skill when orchestrating the retained "ilmn_3u_filter_out_aTARs" step of the mckellardw slide_snake finish finish workflow. It keeps the ilmn 3u filter out aTARs stage tied to upstream `ilmn_3u_calcHMMbed` and the downstream handoff to `ilmn_3u_bed_to_gtf`. It tracks completion via `results/finish/ilmn_3u_filter_out_aTARs.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ilmn_3u_filter_out_aTARs
  step_name: ilmn 3u filter out aTARs
---

# Scope
Use this skill only for the `ilmn_3u_filter_out_aTARs` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ilmn_3u_calcHMMbed`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ilmn_3u_filter_out_aTARs.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ilmn_3u_filter_out_aTARs.done`
- Representative outputs: `results/finish/ilmn_3u_filter_out_aTARs.done`
- Execution targets: `ilmn_3u_filter_out_aTARs`
- Downstream handoff: `ilmn_3u_bed_to_gtf`

## Guardrails
- Treat `results/finish/ilmn_3u_filter_out_aTARs.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ilmn_3u_filter_out_aTARs.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ilmn_3u_bed_to_gtf` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ilmn_3u_filter_out_aTARs.done` exists and `ilmn_3u_bed_to_gtf` can proceed without re-running ilmn 3u filter out aTARs.
