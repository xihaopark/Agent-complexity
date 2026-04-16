---
name: finish-lwang-genomics-ngs-pipeline-sn-rna-seq-convert_bw
description: Use this skill when orchestrating the retained "convert_bw" step of the lwang genomics ngs_pipeline_sn rna_seq finish finish workflow. It keeps the convert bw stage tied to upstream `filter_sort_index` and the downstream handoff to `count_gene`. It tracks completion via `results/finish/convert_bw.done`.
metadata:
  workflow_id: lwang-genomics-ngs_pipeline_sn-rna_seq-finish
  workflow_name: lwang genomics ngs_pipeline_sn rna_seq finish
  step_id: convert_bw
  step_name: convert bw
---

# Scope
Use this skill only for the `convert_bw` step in `lwang-genomics-ngs_pipeline_sn-rna_seq-finish`.

## Orchestration
- Upstream requirements: `filter_sort_index`
- Step file: `finish/lwang-genomics-ngs_pipeline_sn-rna_seq-finish/steps/convert_bw.smk`
- Config file: `finish/lwang-genomics-ngs_pipeline_sn-rna_seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/convert_bw.done`
- Representative outputs: `results/finish/convert_bw.done`
- Execution targets: `convert_bw`
- Downstream handoff: `count_gene`

## Guardrails
- Treat `results/finish/convert_bw.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/convert_bw.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `count_gene` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/convert_bw.done` exists and `count_gene` can proceed without re-running convert bw.
