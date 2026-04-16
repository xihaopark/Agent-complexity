---
name: finish-snakemake-workflows-cellranger-count-create_cellranger_library_csv
description: Use this skill when orchestrating the retained "create_cellranger_library_csv" step of the snakemake workflows cellranger count finish finish workflow. It keeps the create cellranger library csv stage tied to upstream `follow_pedantic_cell_ranger_naming_scheme` and the downstream handoff to `cellranger_count`. It tracks completion via `results/finish/create_cellranger_library_csv.done`.
metadata:
  workflow_id: cellranger-count-finish
  workflow_name: snakemake workflows cellranger count finish
  step_id: create_cellranger_library_csv
  step_name: create cellranger library csv
---

# Scope
Use this skill only for the `create_cellranger_library_csv` step in `cellranger-count-finish`.

## Orchestration
- Upstream requirements: `follow_pedantic_cell_ranger_naming_scheme`
- Step file: `finish/cellranger-count-finish/steps/create_cellranger_library_csv.smk`
- Config file: `finish/cellranger-count-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/create_cellranger_library_csv.done`
- Representative outputs: `results/finish/create_cellranger_library_csv.done`
- Execution targets: `create_cellranger_library_csv`
- Downstream handoff: `cellranger_count`

## Guardrails
- Treat `results/finish/create_cellranger_library_csv.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/create_cellranger_library_csv.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `cellranger_count` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/create_cellranger_library_csv.done` exists and `cellranger_count` can proceed without re-running create cellranger library csv.
