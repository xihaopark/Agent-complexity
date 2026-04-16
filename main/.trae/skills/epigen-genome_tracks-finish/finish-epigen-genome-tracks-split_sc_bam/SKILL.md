---
name: finish-epigen-genome-tracks-split_sc_bam
description: Use this skill when orchestrating the retained "split_sc_bam" step of the epigen genome_tracks finish finish workflow. It keeps the split sc bam stage tied to upstream `make_bed` and the downstream handoff to `merge_bams`. It tracks completion via `results/finish/split_sc_bam.done`.
metadata:
  workflow_id: epigen-genome_tracks-finish
  workflow_name: epigen genome_tracks finish
  step_id: split_sc_bam
  step_name: split sc bam
---

# Scope
Use this skill only for the `split_sc_bam` step in `epigen-genome_tracks-finish`.

## Orchestration
- Upstream requirements: `make_bed`
- Step file: `finish/epigen-genome_tracks-finish/steps/split_sc_bam.smk`
- Config file: `finish/epigen-genome_tracks-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/split_sc_bam.done`
- Representative outputs: `results/finish/split_sc_bam.done`
- Execution targets: `split_sc_bam`
- Downstream handoff: `merge_bams`

## Guardrails
- Treat `results/finish/split_sc_bam.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/split_sc_bam.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `merge_bams` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/split_sc_bam.done` exists and `merge_bams` can proceed without re-running split sc bam.
