---
name: finish-snakemake-workflows-dna-seq-short-read-circle-map-merge_unit_bams_per_sample
description: Use this skill when orchestrating the retained "merge_unit_bams_per_sample" step of the snakemake workflows dna seq short read circle map finish finish workflow. It keeps the merge unit bams per sample stage tied to upstream `bwa_mem` and the downstream handoff to `recalibrate_base_qualities`. It tracks completion via `results/finish/merge_unit_bams_per_sample.done`.
metadata:
  workflow_id: dna-seq-short-read-circle-map-finish
  workflow_name: snakemake workflows dna seq short read circle map finish
  step_id: merge_unit_bams_per_sample
  step_name: merge unit bams per sample
---

# Scope
Use this skill only for the `merge_unit_bams_per_sample` step in `dna-seq-short-read-circle-map-finish`.

## Orchestration
- Upstream requirements: `bwa_mem`
- Step file: `finish/dna-seq-short-read-circle-map-finish/steps/merge_unit_bams_per_sample.smk`
- Config file: `finish/dna-seq-short-read-circle-map-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/merge_unit_bams_per_sample.done`
- Representative outputs: `results/finish/merge_unit_bams_per_sample.done`
- Execution targets: `merge_unit_bams_per_sample`
- Downstream handoff: `recalibrate_base_qualities`

## Guardrails
- Treat `results/finish/merge_unit_bams_per_sample.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/merge_unit_bams_per_sample.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `recalibrate_base_qualities` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/merge_unit_bams_per_sample.done` exists and `recalibrate_base_qualities` can proceed without re-running merge unit bams per sample.
