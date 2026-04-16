---
name: finish-epigen-genome-tracks-igv_report
description: Use this skill when orchestrating the retained "igv_report" step of the epigen genome_tracks finish finish workflow. It keeps the igv report stage tied to upstream `plot_tracks` and the downstream handoff to `all`. It tracks completion via `results/finish/igv_report.done`.
metadata:
  workflow_id: epigen-genome_tracks-finish
  workflow_name: epigen genome_tracks finish
  step_id: igv_report
  step_name: igv report
---

# Scope
Use this skill only for the `igv_report` step in `epigen-genome_tracks-finish`.

## Orchestration
- Upstream requirements: `plot_tracks`
- Step file: `finish/epigen-genome_tracks-finish/steps/igv_report.smk`
- Config file: `finish/epigen-genome_tracks-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/igv_report.done`
- Representative outputs: `results/finish/igv_report.done`
- Execution targets: `igv_report`
- Downstream handoff: `all`

## Guardrails
- Treat `results/finish/igv_report.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/igv_report.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `all` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/igv_report.done` exists and `all` can proceed without re-running igv report.
