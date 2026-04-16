---
name: finish-mckellardw-slide-snake-ont_2a_filter_bam_empty_tags
description: Use this skill when orchestrating the retained "ont_2a_filter_bam_empty_tags" step of the mckellardw slide_snake finish finish workflow. It keeps the ont 2a filter bam empty tags stage tied to upstream `ont_2a_add_umis` and the downstream handoff to `ont_2a_featureCounts`. It tracks completion via `results/finish/ont_2a_filter_bam_empty_tags.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ont_2a_filter_bam_empty_tags
  step_name: ont 2a filter bam empty tags
---

# Scope
Use this skill only for the `ont_2a_filter_bam_empty_tags` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ont_2a_add_umis`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ont_2a_filter_bam_empty_tags.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ont_2a_filter_bam_empty_tags.done`
- Representative outputs: `results/finish/ont_2a_filter_bam_empty_tags.done`
- Execution targets: `ont_2a_filter_bam_empty_tags`
- Downstream handoff: `ont_2a_featureCounts`

## Guardrails
- Treat `results/finish/ont_2a_filter_bam_empty_tags.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ont_2a_filter_bam_empty_tags.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ont_2a_featureCounts` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ont_2a_filter_bam_empty_tags.done` exists and `ont_2a_featureCounts` can proceed without re-running ont 2a filter bam empty tags.
