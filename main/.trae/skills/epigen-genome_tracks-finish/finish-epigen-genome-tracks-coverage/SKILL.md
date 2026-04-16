---
name: finish-epigen-genome-tracks-coverage
description: Use this skill when orchestrating the retained "coverage" step of the epigen genome_tracks finish finish workflow. It keeps the coverage stage tied to upstream `merge_bams` and the downstream handoff to `ucsc_hub`. It tracks completion via `results/finish/coverage.done`.
metadata:
  workflow_id: epigen-genome_tracks-finish
  workflow_name: epigen genome_tracks finish
  step_id: coverage
  step_name: coverage
---

# Scope
Use this skill only for the `coverage` step in `epigen-genome_tracks-finish`.

## Orchestration
- Upstream requirements: `merge_bams`
- Step file: `finish/epigen-genome_tracks-finish/steps/coverage.smk`
- Config file: `finish/epigen-genome_tracks-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/coverage.done`
- Representative outputs: `results/finish/coverage.done`
- Execution targets: `coverage`
- Downstream handoff: `ucsc_hub`

## Guardrails
- Treat `results/finish/coverage.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/coverage.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ucsc_hub` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/coverage.done` exists and `ucsc_hub` can proceed without re-running coverage.
