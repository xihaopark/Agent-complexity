---
name: finish-lwang-genomics-ngs-pipeline-sn-rna-seq-filter_sort_index
description: Use this skill when orchestrating the retained "filter_sort_index" step of the lwang genomics ngs_pipeline_sn rna_seq finish finish workflow. It keeps the filter sort index stage tied to upstream `align` and the downstream handoff to `convert_bw`. It tracks completion via `results/finish/filter_sort_index.done`.
metadata:
  workflow_id: lwang-genomics-ngs_pipeline_sn-rna_seq-finish
  workflow_name: lwang genomics ngs_pipeline_sn rna_seq finish
  step_id: filter_sort_index
  step_name: filter sort index
---

# Scope
Use this skill only for the `filter_sort_index` step in `lwang-genomics-ngs_pipeline_sn-rna_seq-finish`.

## Orchestration
- Upstream requirements: `align`
- Step file: `finish/lwang-genomics-ngs_pipeline_sn-rna_seq-finish/steps/filter_sort_index.smk`
- Config file: `finish/lwang-genomics-ngs_pipeline_sn-rna_seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/filter_sort_index.done`
- Representative outputs: `results/finish/filter_sort_index.done`
- Execution targets: `filter_sort_index`
- Downstream handoff: `convert_bw`

## Guardrails
- Treat `results/finish/filter_sort_index.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/filter_sort_index.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `convert_bw` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/filter_sort_index.done` exists and `convert_bw` can proceed without re-running filter sort index.
