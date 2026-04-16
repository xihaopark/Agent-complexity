---
name: finish-snakemake-workflows-cellranger-multi-cellranger_multi_files_vdj_global
description: Use this skill when orchestrating the retained "cellranger_multi_files_vdj_global" step of the snakemake workflows cellranger multi finish finish workflow. It keeps the cellranger multi files vdj global stage tied to upstream `cellranger_multi_files_vdj_reference` and the downstream handoff to `cellranger_multi_files_vdj_per_sample`. It tracks completion via `results/finish/cellranger_multi_files_vdj_global.done`.
metadata:
  workflow_id: cellranger-multi-finish
  workflow_name: snakemake workflows cellranger multi finish
  step_id: cellranger_multi_files_vdj_global
  step_name: cellranger multi files vdj global
---

# Scope
Use this skill only for the `cellranger_multi_files_vdj_global` step in `cellranger-multi-finish`.

## Orchestration
- Upstream requirements: `cellranger_multi_files_vdj_reference`
- Step file: `finish/cellranger-multi-finish/steps/cellranger_multi_files_vdj_global.smk`
- Config file: `finish/cellranger-multi-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/cellranger_multi_files_vdj_global.done`
- Representative outputs: `results/finish/cellranger_multi_files_vdj_global.done`
- Execution targets: `cellranger_multi_files_vdj_global`
- Downstream handoff: `cellranger_multi_files_vdj_per_sample`

## Guardrails
- Treat `results/finish/cellranger_multi_files_vdj_global.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/cellranger_multi_files_vdj_global.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `cellranger_multi_files_vdj_per_sample` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/cellranger_multi_files_vdj_global.done` exists and `cellranger_multi_files_vdj_per_sample` can proceed without re-running cellranger multi files vdj global.
