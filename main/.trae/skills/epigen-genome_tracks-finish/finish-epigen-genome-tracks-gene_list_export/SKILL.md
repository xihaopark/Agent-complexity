---
name: finish-epigen-genome-tracks-gene_list_export
description: Use this skill when orchestrating the retained "gene_list_export" step of the epigen genome_tracks finish finish workflow. It keeps the gene list export stage tied to upstream `annot_export` and the downstream handoff to `make_bed`. It tracks completion via `results/finish/gene_list_export.done`.
metadata:
  workflow_id: epigen-genome_tracks-finish
  workflow_name: epigen genome_tracks finish
  step_id: gene_list_export
  step_name: gene list export
---

# Scope
Use this skill only for the `gene_list_export` step in `epigen-genome_tracks-finish`.

## Orchestration
- Upstream requirements: `annot_export`
- Step file: `finish/epigen-genome_tracks-finish/steps/gene_list_export.smk`
- Config file: `finish/epigen-genome_tracks-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/gene_list_export.done`
- Representative outputs: `results/finish/gene_list_export.done`
- Execution targets: `gene_list_export`
- Downstream handoff: `make_bed`

## Guardrails
- Treat `results/finish/gene_list_export.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/gene_list_export.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `make_bed` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/gene_list_export.done` exists and `make_bed` can proceed without re-running gene list export.
