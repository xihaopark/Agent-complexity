---
name: finish-snakemake-workflows-cellranger-multi-cellranger_multi_files_vdj_per_sample
description: Use this skill when orchestrating the retained "cellranger_multi_files_vdj_per_sample" step of the snakemake workflows cellranger multi finish finish workflow. It keeps the cellranger multi files vdj per sample stage tied to upstream `cellranger_multi_files_vdj_global` and the downstream handoff to `all`. It tracks completion via `results/finish/cellranger_multi_files_vdj_per_sample.done`.
metadata:
  workflow_id: cellranger-multi-finish
  workflow_name: snakemake workflows cellranger multi finish
  step_id: cellranger_multi_files_vdj_per_sample
  step_name: cellranger multi files vdj per sample
---

# Scope
Use this skill only for the `cellranger_multi_files_vdj_per_sample` step in `cellranger-multi-finish`.

## Orchestration
- Upstream requirements: `cellranger_multi_files_vdj_global`
- Step file: `finish/cellranger-multi-finish/steps/cellranger_multi_files_vdj_per_sample.smk`
- Config file: `finish/cellranger-multi-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/cellranger_multi_files_vdj_per_sample.done`
- Representative outputs: `results/finish/cellranger_multi_files_vdj_per_sample.done`
- Execution targets: `cellranger_multi_files_vdj_per_sample`
- Downstream handoff: `all`

## Guardrails
- Treat `results/finish/cellranger_multi_files_vdj_per_sample.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/cellranger_multi_files_vdj_per_sample.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `all` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/cellranger_multi_files_vdj_per_sample.done` exists and `all` can proceed without re-running cellranger multi files vdj per sample.
