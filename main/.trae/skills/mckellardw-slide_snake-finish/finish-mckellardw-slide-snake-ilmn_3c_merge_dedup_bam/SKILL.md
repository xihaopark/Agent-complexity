---
name: finish-mckellardw-slide-snake-ilmn_3c_merge_dedup_bam
description: Use this skill when orchestrating the retained "ilmn_3c_merge_dedup_bam" step of the mckellardw slide_snake finish finish workflow. It keeps the ilmn 3c merge dedup bam stage tied to upstream `ilmn_3c_umitools_dedup_revBAM` and the downstream handoff to `ilmn_3q_qualimapQC_STAR`. It tracks completion via `results/finish/ilmn_3c_merge_dedup_bam.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ilmn_3c_merge_dedup_bam
  step_name: ilmn 3c merge dedup bam
---

# Scope
Use this skill only for the `ilmn_3c_merge_dedup_bam` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ilmn_3c_umitools_dedup_revBAM`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ilmn_3c_merge_dedup_bam.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ilmn_3c_merge_dedup_bam.done`
- Representative outputs: `results/finish/ilmn_3c_merge_dedup_bam.done`
- Execution targets: `ilmn_3c_merge_dedup_bam`
- Downstream handoff: `ilmn_3q_qualimapQC_STAR`

## Guardrails
- Treat `results/finish/ilmn_3c_merge_dedup_bam.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ilmn_3c_merge_dedup_bam.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ilmn_3q_qualimapQC_STAR` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ilmn_3c_merge_dedup_bam.done` exists and `ilmn_3q_qualimapQC_STAR` can proceed without re-running ilmn 3c merge dedup bam.
