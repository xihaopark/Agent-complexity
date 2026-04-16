---
name: finish-tgirke-systempiperdata-spscrna-qc_seurat
description: Use this skill when orchestrating the retained "qc_seurat" step of the tgirke systempiperdata spscrna finish finish workflow. It keeps the qc seurat stage tied to upstream `create_seurat` and the downstream handoff to `filter_cells`. It tracks completion via `results/finish/qc_seurat.done`.
metadata:
  workflow_id: tgirke-systempiperdata-spscrna-finish
  workflow_name: tgirke systempiperdata spscrna finish
  step_id: qc_seurat
  step_name: qc seurat
---

# Scope
Use this skill only for the `qc_seurat` step in `tgirke-systempiperdata-spscrna-finish`.

## Orchestration
- Upstream requirements: `create_seurat`
- Step file: `finish/tgirke-systempiperdata-spscrna-finish/steps/qc_seurat.smk`
- Config file: `finish/tgirke-systempiperdata-spscrna-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/qc_seurat.done`
- Representative outputs: `results/finish/qc_seurat.done`
- Execution targets: `qc_seurat`
- Downstream handoff: `filter_cells`

## Guardrails
- Treat `results/finish/qc_seurat.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/qc_seurat.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `filter_cells` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/qc_seurat.done` exists and `filter_cells` can proceed without re-running qc seurat.
