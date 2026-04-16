---
name: finish-snakemake-workflows-cellranger-multi-create_cellranger_multi_config_csv
description: Use this skill when orchestrating the retained "create_cellranger_multi_config_csv" step of the snakemake workflows cellranger multi finish finish workflow. It keeps the create cellranger multi config csv stage tied to upstream `follow_pedantic_cell_ranger_naming_scheme` and the downstream handoff to `cellranger_multi_run`. It tracks completion via `results/finish/create_cellranger_multi_config_csv.done`.
metadata:
  workflow_id: cellranger-multi-finish
  workflow_name: snakemake workflows cellranger multi finish
  step_id: create_cellranger_multi_config_csv
  step_name: create cellranger multi config csv
---

# Scope
Use this skill only for the `create_cellranger_multi_config_csv` step in `cellranger-multi-finish`.

## Orchestration
- Upstream requirements: `follow_pedantic_cell_ranger_naming_scheme`
- Step file: `finish/cellranger-multi-finish/steps/create_cellranger_multi_config_csv.smk`
- Config file: `finish/cellranger-multi-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/create_cellranger_multi_config_csv.done`
- Representative outputs: `results/finish/create_cellranger_multi_config_csv.done`
- Execution targets: `create_cellranger_multi_config_csv`
- Downstream handoff: `cellranger_multi_run`

## Guardrails
- Treat `results/finish/create_cellranger_multi_config_csv.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/create_cellranger_multi_config_csv.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `cellranger_multi_run` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/create_cellranger_multi_config_csv.done` exists and `cellranger_multi_run` can proceed without re-running create cellranger multi config csv.
