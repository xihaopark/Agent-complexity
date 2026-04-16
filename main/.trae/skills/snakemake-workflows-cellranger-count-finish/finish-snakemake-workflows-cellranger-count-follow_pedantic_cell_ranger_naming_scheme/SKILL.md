---
name: finish-snakemake-workflows-cellranger-count-follow_pedantic_cell_ranger_naming_scheme
description: Use this skill when orchestrating the retained "follow_pedantic_cell_ranger_naming_scheme" step of the snakemake workflows cellranger count finish finish workflow. It keeps the follow pedantic cell ranger naming scheme stage and the downstream handoff to `create_cellranger_library_csv`. It tracks completion via `results/finish/follow_pedantic_cell_ranger_naming_scheme.done`.
metadata:
  workflow_id: cellranger-count-finish
  workflow_name: snakemake workflows cellranger count finish
  step_id: follow_pedantic_cell_ranger_naming_scheme
  step_name: follow pedantic cell ranger naming scheme
---

# Scope
Use this skill only for the `follow_pedantic_cell_ranger_naming_scheme` step in `cellranger-count-finish`.

## Orchestration
- Upstream requirements: none
- Step file: `finish/cellranger-count-finish/steps/follow_pedantic_cell_ranger_naming_scheme.smk`
- Config file: `finish/cellranger-count-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/follow_pedantic_cell_ranger_naming_scheme.done`
- Representative outputs: `results/finish/follow_pedantic_cell_ranger_naming_scheme.done`
- Execution targets: `follow_pedantic_cell_ranger_naming_scheme`
- Downstream handoff: `create_cellranger_library_csv`

## Guardrails
- Treat `results/finish/follow_pedantic_cell_ranger_naming_scheme.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/follow_pedantic_cell_ranger_naming_scheme.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `create_cellranger_library_csv` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/follow_pedantic_cell_ranger_naming_scheme.done` exists and `create_cellranger_library_csv` can proceed without re-running follow pedantic cell ranger naming scheme.
