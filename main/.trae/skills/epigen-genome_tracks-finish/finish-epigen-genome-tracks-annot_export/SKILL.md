---
name: finish-epigen-genome-tracks-annot_export
description: Use this skill when orchestrating the retained "annot_export" step of the epigen genome_tracks finish finish workflow. It keeps the annot export stage tied to upstream `config_export` and the downstream handoff to `gene_list_export`. It tracks completion via `results/finish/annot_export.done`.
metadata:
  workflow_id: epigen-genome_tracks-finish
  workflow_name: epigen genome_tracks finish
  step_id: annot_export
  step_name: annot export
---

# Scope
Use this skill only for the `annot_export` step in `epigen-genome_tracks-finish`.

## Orchestration
- Upstream requirements: `config_export`
- Step file: `finish/epigen-genome_tracks-finish/steps/annot_export.smk`
- Config file: `finish/epigen-genome_tracks-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/annot_export.done`
- Representative outputs: `results/finish/annot_export.done`
- Execution targets: `annot_export`
- Downstream handoff: `gene_list_export`

## Guardrails
- Treat `results/finish/annot_export.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/annot_export.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `gene_list_export` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/annot_export.done` exists and `gene_list_export` can proceed without re-running annot export.
