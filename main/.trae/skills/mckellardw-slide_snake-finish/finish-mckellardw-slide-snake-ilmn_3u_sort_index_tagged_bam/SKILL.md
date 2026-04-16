---
name: finish-mckellardw-slide-snake-ilmn_3u_sort_index_tagged_bam
description: Use this skill when orchestrating the retained "ilmn_3u_sort_index_tagged_bam" step of the mckellardw slide_snake finish finish workflow. It keeps the ilmn 3u sort index tagged bam stage tied to upstream `ilmn_3u_tagReads` and the downstream handoff to `ilmn_3u_extract_HMM_expression`. It tracks completion via `results/finish/ilmn_3u_sort_index_tagged_bam.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ilmn_3u_sort_index_tagged_bam
  step_name: ilmn 3u sort index tagged bam
---

# Scope
Use this skill only for the `ilmn_3u_sort_index_tagged_bam` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ilmn_3u_tagReads`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ilmn_3u_sort_index_tagged_bam.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ilmn_3u_sort_index_tagged_bam.done`
- Representative outputs: `results/finish/ilmn_3u_sort_index_tagged_bam.done`
- Execution targets: `ilmn_3u_sort_index_tagged_bam`
- Downstream handoff: `ilmn_3u_extract_HMM_expression`

## Guardrails
- Treat `results/finish/ilmn_3u_sort_index_tagged_bam.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ilmn_3u_sort_index_tagged_bam.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ilmn_3u_extract_HMM_expression` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ilmn_3u_sort_index_tagged_bam.done` exists and `ilmn_3u_extract_HMM_expression` can proceed without re-running ilmn 3u sort index tagged bam.
