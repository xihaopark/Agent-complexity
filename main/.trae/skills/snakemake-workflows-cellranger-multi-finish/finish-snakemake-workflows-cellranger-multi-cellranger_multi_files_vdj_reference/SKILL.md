---
name: finish-snakemake-workflows-cellranger-multi-cellranger_multi_files_vdj_reference
description: Use this skill when orchestrating the retained "cellranger_multi_files_vdj_reference" step of the snakemake workflows cellranger multi finish finish workflow. It keeps the cellranger multi files vdj reference stage tied to upstream `cellranger_multi_files_gene_expression_per_sample` and the downstream handoff to `cellranger_multi_files_vdj_global`. It tracks completion via `results/finish/cellranger_multi_files_vdj_reference.done`.
metadata:
  workflow_id: cellranger-multi-finish
  workflow_name: snakemake workflows cellranger multi finish
  step_id: cellranger_multi_files_vdj_reference
  step_name: cellranger multi files vdj reference
---

# Scope
Use this skill only for the `cellranger_multi_files_vdj_reference` step in `cellranger-multi-finish`.

## Orchestration
- Upstream requirements: `cellranger_multi_files_gene_expression_per_sample`
- Step file: `finish/cellranger-multi-finish/steps/cellranger_multi_files_vdj_reference.smk`
- Config file: `finish/cellranger-multi-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/cellranger_multi_files_vdj_reference.done`
- Representative outputs: `results/finish/cellranger_multi_files_vdj_reference.done`
- Execution targets: `cellranger_multi_files_vdj_reference`
- Downstream handoff: `cellranger_multi_files_vdj_global`

## Guardrails
- Treat `results/finish/cellranger_multi_files_vdj_reference.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/cellranger_multi_files_vdj_reference.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `cellranger_multi_files_vdj_global` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/cellranger_multi_files_vdj_reference.done` exists and `cellranger_multi_files_vdj_global` can proceed without re-running cellranger multi files vdj reference.
