---
name: finish-mckellardw-slide-snake-ont_2d_ultra_add_featurecounts_to_bam
description: Use this skill when orchestrating the retained "ont_2d_ultra_add_featureCounts_to_bam" step of the mckellardw slide_snake finish finish workflow. It keeps the ont 2d ultra add featureCounts to bam stage tied to upstream `ont_2d_ultra_featureCounts` and the downstream handoff to `ont_2d_ultra_umitools_count`. It tracks completion via `results/finish/ont_2d_ultra_add_featureCounts_to_bam.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ont_2d_ultra_add_featureCounts_to_bam
  step_name: ont 2d ultra add featureCounts to bam
---

# Scope
Use this skill only for the `ont_2d_ultra_add_featureCounts_to_bam` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ont_2d_ultra_featureCounts`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ont_2d_ultra_add_featureCounts_to_bam.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ont_2d_ultra_add_featureCounts_to_bam.done`
- Representative outputs: `results/finish/ont_2d_ultra_add_featureCounts_to_bam.done`
- Execution targets: `ont_2d_ultra_add_featureCounts_to_bam`
- Downstream handoff: `ont_2d_ultra_umitools_count`

## Guardrails
- Treat `results/finish/ont_2d_ultra_add_featureCounts_to_bam.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ont_2d_ultra_add_featureCounts_to_bam.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ont_2d_ultra_umitools_count` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ont_2d_ultra_add_featureCounts_to_bam.done` exists and `ont_2d_ultra_umitools_count` can proceed without re-running ont 2d ultra add featureCounts to bam.
