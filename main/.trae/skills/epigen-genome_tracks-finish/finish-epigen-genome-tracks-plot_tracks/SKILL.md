---
name: finish-epigen-genome-tracks-plot_tracks
description: Use this skill when orchestrating the retained "plot_tracks" step of the epigen genome_tracks finish finish workflow. It keeps the plot tracks stage tied to upstream `ucsc_hub` and the downstream handoff to `igv_report`. It tracks completion via `results/finish/plot_tracks.done`.
metadata:
  workflow_id: epigen-genome_tracks-finish
  workflow_name: epigen genome_tracks finish
  step_id: plot_tracks
  step_name: plot tracks
---

# Scope
Use this skill only for the `plot_tracks` step in `epigen-genome_tracks-finish`.

## Orchestration
- Upstream requirements: `ucsc_hub`
- Step file: `finish/epigen-genome_tracks-finish/steps/plot_tracks.smk`
- Config file: `finish/epigen-genome_tracks-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plot_tracks.done`
- Representative outputs: `results/finish/plot_tracks.done`
- Execution targets: `plot_tracks`
- Downstream handoff: `igv_report`

## Guardrails
- Treat `results/finish/plot_tracks.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plot_tracks.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `igv_report` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plot_tracks.done` exists and `igv_report` can proceed without re-running plot tracks.
