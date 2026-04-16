---
name: finish-snakemake-workflows-cellranger-multi-cellranger_multi_run
description: Use this skill when orchestrating the retained "cellranger_multi_run" step of the snakemake workflows cellranger multi finish finish workflow. It keeps the cellranger multi run stage tied to upstream `create_cellranger_multi_config_csv` and the downstream handoff to `cellranger_multi_files_summaries`. It tracks completion via `results/finish/cellranger_multi_run.done`.
metadata:
  workflow_id: cellranger-multi-finish
  workflow_name: snakemake workflows cellranger multi finish
  step_id: cellranger_multi_run
  step_name: cellranger multi run
---

# Scope
Use this skill only for the `cellranger_multi_run` step in `cellranger-multi-finish`.

## Orchestration
- Upstream requirements: `create_cellranger_multi_config_csv`
- Step file: `finish/cellranger-multi-finish/steps/cellranger_multi_run.smk`
- Config file: `finish/cellranger-multi-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/cellranger_multi_run.done`
- Representative outputs: `results/finish/cellranger_multi_run.done`
- Execution targets: `cellranger_multi_run`
- Downstream handoff: `cellranger_multi_files_summaries`

## Guardrails
- Treat `results/finish/cellranger_multi_run.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/cellranger_multi_run.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `cellranger_multi_files_summaries` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/cellranger_multi_run.done` exists and `cellranger_multi_files_summaries` can proceed without re-running cellranger multi run.
