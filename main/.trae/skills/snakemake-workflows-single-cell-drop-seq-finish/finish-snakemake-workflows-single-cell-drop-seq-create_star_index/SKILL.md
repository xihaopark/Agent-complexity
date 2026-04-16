---
name: finish-snakemake-workflows-single-cell-drop-seq-create_star_index
description: Use this skill when orchestrating the retained "create_star_index" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the create star index stage tied to upstream `prep_star_index` and the downstream handoff to `fastqc_barcodes`. It tracks completion via `results/finish/create_star_index.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: create_star_index
  step_name: create star index
---

# Scope
Use this skill only for the `create_star_index` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `prep_star_index`
- Step file: `finish/single-cell-drop-seq-finish/steps/create_star_index.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/create_star_index.done`
- Representative outputs: `results/finish/create_star_index.done`
- Execution targets: `create_star_index`
- Downstream handoff: `fastqc_barcodes`

## Guardrails
- Treat `results/finish/create_star_index.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/create_star_index.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `fastqc_barcodes` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/create_star_index.done` exists and `fastqc_barcodes` can proceed without re-running create star index.
