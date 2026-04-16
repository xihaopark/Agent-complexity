---
name: finish-tgirke-systempiperdata-spscrna-filter_cells
description: Use this skill when orchestrating the retained "filter_cells" step of the tgirke systempiperdata spscrna finish finish workflow. It keeps the filter cells stage tied to upstream `qc_seurat` and the downstream handoff to `normalize`. It tracks completion via `results/finish/filter_cells.done`.
metadata:
  workflow_id: tgirke-systempiperdata-spscrna-finish
  workflow_name: tgirke systempiperdata spscrna finish
  step_id: filter_cells
  step_name: filter cells
---

# Scope
Use this skill only for the `filter_cells` step in `tgirke-systempiperdata-spscrna-finish`.

## Orchestration
- Upstream requirements: `qc_seurat`
- Step file: `finish/tgirke-systempiperdata-spscrna-finish/steps/filter_cells.smk`
- Config file: `finish/tgirke-systempiperdata-spscrna-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/filter_cells.done`
- Representative outputs: `results/finish/filter_cells.done`
- Execution targets: `filter_cells`
- Downstream handoff: `normalize`

## Guardrails
- Treat `results/finish/filter_cells.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/filter_cells.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `normalize` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/filter_cells.done` exists and `normalize` can proceed without re-running filter cells.
