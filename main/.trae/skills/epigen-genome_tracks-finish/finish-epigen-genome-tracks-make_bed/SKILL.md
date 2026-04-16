---
name: finish-epigen-genome-tracks-make_bed
description: Use this skill when orchestrating the retained "make_bed" step of the epigen genome_tracks finish finish workflow. It keeps the make bed stage tied to upstream `gene_list_export` and the downstream handoff to `split_sc_bam`. It tracks completion via `results/finish/make_bed.done`.
metadata:
  workflow_id: epigen-genome_tracks-finish
  workflow_name: epigen genome_tracks finish
  step_id: make_bed
  step_name: make bed
---

# Scope
Use this skill only for the `make_bed` step in `epigen-genome_tracks-finish`.

## Orchestration
- Upstream requirements: `gene_list_export`
- Step file: `finish/epigen-genome_tracks-finish/steps/make_bed.smk`
- Config file: `finish/epigen-genome_tracks-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/make_bed.done`
- Representative outputs: `results/finish/make_bed.done`
- Execution targets: `make_bed`
- Downstream handoff: `split_sc_bam`

## Guardrails
- Treat `results/finish/make_bed.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/make_bed.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `split_sc_bam` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/make_bed.done` exists and `split_sc_bam` can proceed without re-running make bed.
