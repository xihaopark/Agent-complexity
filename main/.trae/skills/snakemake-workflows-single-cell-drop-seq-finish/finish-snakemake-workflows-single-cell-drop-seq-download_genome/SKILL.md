---
name: finish-snakemake-workflows-single-cell-drop-seq-download_genome
description: Use this skill when orchestrating the retained "download_genome" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the download genome stage tied to upstream `download_annotation` and the downstream handoff to `rename_genome`. It tracks completion via `results/finish/download_genome.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: download_genome
  step_name: download genome
---

# Scope
Use this skill only for the `download_genome` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `download_annotation`
- Step file: `finish/single-cell-drop-seq-finish/steps/download_genome.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/download_genome.done`
- Representative outputs: `results/finish/download_genome.done`
- Execution targets: `download_genome`
- Downstream handoff: `rename_genome`

## Guardrails
- Treat `results/finish/download_genome.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/download_genome.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `rename_genome` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/download_genome.done` exists and `rename_genome` can proceed without re-running download genome.
