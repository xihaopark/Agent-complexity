---
name: finish-lwang-genomics-ngs-pipeline-sn-atac-seq-remove_mito
description: Use this skill when orchestrating the retained "remove_mito" step of the lwang genomics ngs_pipeline_sn atac_seq finish finish workflow. It keeps the remove mito stage tied to upstream `align` and the downstream handoff to `filter_sort_index`. It tracks completion via `results/finish/remove_mito.done`.
metadata:
  workflow_id: lwang-genomics-ngs_pipeline_sn-atac_seq-finish
  workflow_name: lwang genomics ngs_pipeline_sn atac_seq finish
  step_id: remove_mito
  step_name: remove mito
---

# Scope
Use this skill only for the `remove_mito` step in `lwang-genomics-ngs_pipeline_sn-atac_seq-finish`.

## Orchestration
- Upstream requirements: `align`
- Step file: `finish/lwang-genomics-ngs_pipeline_sn-atac_seq-finish/steps/remove_mito.smk`
- Config file: `finish/lwang-genomics-ngs_pipeline_sn-atac_seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/remove_mito.done`
- Representative outputs: `results/finish/remove_mito.done`
- Execution targets: `remove_mito`
- Downstream handoff: `filter_sort_index`

## Guardrails
- Treat `results/finish/remove_mito.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/remove_mito.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `filter_sort_index` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/remove_mito.done` exists and `filter_sort_index` can proceed without re-running remove mito.
