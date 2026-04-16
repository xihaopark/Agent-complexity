---
name: finish-epigen-genome-tracks-ucsc_hub
description: Use this skill when orchestrating the retained "ucsc_hub" step of the epigen genome_tracks finish finish workflow. It keeps the ucsc hub stage tied to upstream `coverage` and the downstream handoff to `plot_tracks`. It tracks completion via `results/finish/ucsc_hub.done`.
metadata:
  workflow_id: epigen-genome_tracks-finish
  workflow_name: epigen genome_tracks finish
  step_id: ucsc_hub
  step_name: ucsc hub
---

# Scope
Use this skill only for the `ucsc_hub` step in `epigen-genome_tracks-finish`.

## Orchestration
- Upstream requirements: `coverage`
- Step file: `finish/epigen-genome_tracks-finish/steps/ucsc_hub.smk`
- Config file: `finish/epigen-genome_tracks-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ucsc_hub.done`
- Representative outputs: `results/finish/ucsc_hub.done`
- Execution targets: `ucsc_hub`
- Downstream handoff: `plot_tracks`

## Guardrails
- Treat `results/finish/ucsc_hub.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ucsc_hub.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plot_tracks` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ucsc_hub.done` exists and `plot_tracks` can proceed without re-running ucsc hub.
