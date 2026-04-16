---
name: finish-mckellardw-slide-snake-ilmn_3u_bed_to_gtf
description: Use this skill when orchestrating the retained "ilmn_3u_bed_to_gtf" step of the mckellardw slide_snake finish finish workflow. It keeps the ilmn 3u bed to gtf stage tied to upstream `ilmn_3u_filter_out_aTARs` and the downstream handoff to `ilmn_3u_tagReads`. It tracks completion via `results/finish/ilmn_3u_bed_to_gtf.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ilmn_3u_bed_to_gtf
  step_name: ilmn 3u bed to gtf
---

# Scope
Use this skill only for the `ilmn_3u_bed_to_gtf` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ilmn_3u_filter_out_aTARs`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ilmn_3u_bed_to_gtf.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ilmn_3u_bed_to_gtf.done`
- Representative outputs: `results/finish/ilmn_3u_bed_to_gtf.done`
- Execution targets: `ilmn_3u_bed_to_gtf`
- Downstream handoff: `ilmn_3u_tagReads`

## Guardrails
- Treat `results/finish/ilmn_3u_bed_to_gtf.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ilmn_3u_bed_to_gtf.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ilmn_3u_tagReads` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ilmn_3u_bed_to_gtf.done` exists and `ilmn_3u_tagReads` can proceed without re-running ilmn 3u bed to gtf.
