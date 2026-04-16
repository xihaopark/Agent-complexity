---
name: finish-mckellardw-slide-snake-ont_2d_ultra_featurecounts
description: Use this skill when orchestrating the retained "ont_2d_ultra_featureCounts" step of the mckellardw slide_snake finish finish workflow. It keeps the ont 2d ultra featureCounts stage tied to upstream `ont_2d_ultra_filter_bam_empty_tags` and the downstream handoff to `ont_2d_ultra_add_featureCounts_to_bam`. It tracks completion via `results/finish/ont_2d_ultra_featureCounts.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ont_2d_ultra_featureCounts
  step_name: ont 2d ultra featureCounts
---

# Scope
Use this skill only for the `ont_2d_ultra_featureCounts` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ont_2d_ultra_filter_bam_empty_tags`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ont_2d_ultra_featureCounts.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ont_2d_ultra_featureCounts.done`
- Representative outputs: `results/finish/ont_2d_ultra_featureCounts.done`
- Execution targets: `ont_2d_ultra_featureCounts`
- Downstream handoff: `ont_2d_ultra_add_featureCounts_to_bam`

## Guardrails
- Treat `results/finish/ont_2d_ultra_featureCounts.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ont_2d_ultra_featureCounts.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ont_2d_ultra_add_featureCounts_to_bam` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ont_2d_ultra_featureCounts.done` exists and `ont_2d_ultra_add_featureCounts_to_bam` can proceed without re-running ont 2d ultra featureCounts.
