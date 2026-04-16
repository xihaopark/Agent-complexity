---
name: finish-mckellardw-slide-snake-ilmn_3u_tagreads
description: Use this skill when orchestrating the retained "ilmn_3u_tagReads" step of the mckellardw slide_snake finish finish workflow. It keeps the ilmn 3u tagReads stage tied to upstream `ilmn_3u_bed_to_gtf` and the downstream handoff to `ilmn_3u_sort_index_tagged_bam`. It tracks completion via `results/finish/ilmn_3u_tagReads.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ilmn_3u_tagReads
  step_name: ilmn 3u tagReads
---

# Scope
Use this skill only for the `ilmn_3u_tagReads` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ilmn_3u_bed_to_gtf`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ilmn_3u_tagReads.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ilmn_3u_tagReads.done`
- Representative outputs: `results/finish/ilmn_3u_tagReads.done`
- Execution targets: `ilmn_3u_tagReads`
- Downstream handoff: `ilmn_3u_sort_index_tagged_bam`

## Guardrails
- Treat `results/finish/ilmn_3u_tagReads.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ilmn_3u_tagReads.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ilmn_3u_sort_index_tagged_bam` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ilmn_3u_tagReads.done` exists and `ilmn_3u_sort_index_tagged_bam` can proceed without re-running ilmn 3u tagReads.
