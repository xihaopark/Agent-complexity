---
name: finish-tgirke-systempiperdata-spscrna-create_seurat
description: Use this skill when orchestrating the retained "create_seurat" step of the tgirke systempiperdata spscrna finish finish workflow. It keeps the create seurat stage tied to upstream `count_plot` and the downstream handoff to `qc_seurat`. It tracks completion via `results/finish/create_seurat.done`.
metadata:
  workflow_id: tgirke-systempiperdata-spscrna-finish
  workflow_name: tgirke systempiperdata spscrna finish
  step_id: create_seurat
  step_name: create seurat
---

# Scope
Use this skill only for the `create_seurat` step in `tgirke-systempiperdata-spscrna-finish`.

## Orchestration
- Upstream requirements: `count_plot`
- Step file: `finish/tgirke-systempiperdata-spscrna-finish/steps/create_seurat.smk`
- Config file: `finish/tgirke-systempiperdata-spscrna-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/create_seurat.done`
- Representative outputs: `results/finish/create_seurat.done`
- Execution targets: `create_seurat`
- Downstream handoff: `qc_seurat`

## Guardrails
- Treat `results/finish/create_seurat.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/create_seurat.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `qc_seurat` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/create_seurat.done` exists and `qc_seurat` can proceed without re-running create seurat.
