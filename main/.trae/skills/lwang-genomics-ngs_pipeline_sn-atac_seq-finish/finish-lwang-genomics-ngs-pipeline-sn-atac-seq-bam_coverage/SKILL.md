---
name: finish-lwang-genomics-ngs-pipeline-sn-atac-seq-bam_coverage
description: Use this skill when orchestrating the retained "bam_coverage" step of the lwang genomics ngs_pipeline_sn atac_seq finish finish workflow. It keeps the bam coverage stage tied to upstream `filter_sort_index` and the downstream handoff to `call_peaks`. It tracks completion via `results/finish/bam_coverage.done`.
metadata:
  workflow_id: lwang-genomics-ngs_pipeline_sn-atac_seq-finish
  workflow_name: lwang genomics ngs_pipeline_sn atac_seq finish
  step_id: bam_coverage
  step_name: bam coverage
---

# Scope
Use this skill only for the `bam_coverage` step in `lwang-genomics-ngs_pipeline_sn-atac_seq-finish`.

## Orchestration
- Upstream requirements: `filter_sort_index`
- Step file: `finish/lwang-genomics-ngs_pipeline_sn-atac_seq-finish/steps/bam_coverage.smk`
- Config file: `finish/lwang-genomics-ngs_pipeline_sn-atac_seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/bam_coverage.done`
- Representative outputs: `results/finish/bam_coverage.done`
- Execution targets: `bam_coverage`
- Downstream handoff: `call_peaks`

## Guardrails
- Treat `results/finish/bam_coverage.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/bam_coverage.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `call_peaks` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/bam_coverage.done` exists and `call_peaks` can proceed without re-running bam coverage.
