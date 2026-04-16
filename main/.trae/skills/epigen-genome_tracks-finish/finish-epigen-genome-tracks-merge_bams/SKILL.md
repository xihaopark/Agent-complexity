---
name: finish-epigen-genome-tracks-merge_bams
description: Use this skill when orchestrating the retained "merge_bams" step of the epigen genome_tracks finish finish workflow. It keeps the merge bams stage tied to upstream `split_sc_bam` and the downstream handoff to `coverage`. It tracks completion via `results/finish/merge_bams.done`.
metadata:
  workflow_id: epigen-genome_tracks-finish
  workflow_name: epigen genome_tracks finish
  step_id: merge_bams
  step_name: merge bams
---

# Scope
Use this skill only for the `merge_bams` step in `epigen-genome_tracks-finish`.

## Orchestration
- Upstream requirements: `split_sc_bam`
- Step file: `finish/epigen-genome_tracks-finish/steps/merge_bams.smk`
- Config file: `finish/epigen-genome_tracks-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/merge_bams.done`
- Representative outputs: `results/finish/merge_bams.done`
- Execution targets: `merge_bams`
- Downstream handoff: `coverage`

## Guardrails
- Treat `results/finish/merge_bams.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/merge_bams.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `coverage` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/merge_bams.done` exists and `coverage` can proceed without re-running merge bams.
