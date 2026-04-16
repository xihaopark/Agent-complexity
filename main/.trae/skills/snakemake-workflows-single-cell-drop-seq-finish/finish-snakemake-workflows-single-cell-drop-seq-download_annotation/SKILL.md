---
name: finish-snakemake-workflows-single-cell-drop-seq-download_annotation
description: Use this skill when orchestrating the retained "download_annotation" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the download annotation stage tied to upstream `make_report` and the downstream handoff to `download_genome`. It tracks completion via `results/finish/download_annotation.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: download_annotation
  step_name: download annotation
---

# Scope
Use this skill only for the `download_annotation` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `make_report`
- Step file: `finish/single-cell-drop-seq-finish/steps/download_annotation.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/download_annotation.done`
- Representative outputs: `results/finish/download_annotation.done`
- Execution targets: `download_annotation`
- Downstream handoff: `download_genome`

## Guardrails
- Treat `results/finish/download_annotation.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/download_annotation.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `download_genome` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/download_annotation.done` exists and `download_genome` can proceed without re-running download annotation.
