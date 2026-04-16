---
name: finish-mckellardw-slide-snake-ont_2a_split_bam_by_strand
description: Use this skill when orchestrating the retained "ont_2a_split_bam_by_strand" step of the mckellardw slide_snake finish finish workflow. It keeps the ont 2a split bam by strand stage tied to upstream `ont_2a_add_featureCounts_to_bam` and the downstream handoff to `ont_2a_umitools_count`. It tracks completion via `results/finish/ont_2a_split_bam_by_strand.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ont_2a_split_bam_by_strand
  step_name: ont 2a split bam by strand
---

# Scope
Use this skill only for the `ont_2a_split_bam_by_strand` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ont_2a_add_featureCounts_to_bam`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ont_2a_split_bam_by_strand.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ont_2a_split_bam_by_strand.done`
- Representative outputs: `results/finish/ont_2a_split_bam_by_strand.done`
- Execution targets: `ont_2a_split_bam_by_strand`
- Downstream handoff: `ont_2a_umitools_count`

## Guardrails
- Treat `results/finish/ont_2a_split_bam_by_strand.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ont_2a_split_bam_by_strand.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ont_2a_umitools_count` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ont_2a_split_bam_by_strand.done` exists and `ont_2a_umitools_count` can proceed without re-running ont 2a split bam by strand.
