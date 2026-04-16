---
name: finish-lwang-genomics-ngs-pipeline-sn-rna-seq-fastqc_raw
description: Use this skill when orchestrating the retained "fastqc_raw" step of the lwang genomics ngs_pipeline_sn rna_seq finish finish workflow. It keeps the fastqc raw stage and the downstream handoff to `trim`. It tracks completion via `results/finish/fastqc_raw.done`.
metadata:
  workflow_id: lwang-genomics-ngs_pipeline_sn-rna_seq-finish
  workflow_name: lwang genomics ngs_pipeline_sn rna_seq finish
  step_id: fastqc_raw
  step_name: fastqc raw
---

# Scope
Use this skill only for the `fastqc_raw` step in `lwang-genomics-ngs_pipeline_sn-rna_seq-finish`.

## Orchestration
- Upstream requirements: none
- Step file: `finish/lwang-genomics-ngs_pipeline_sn-rna_seq-finish/steps/fastqc_raw.smk`
- Config file: `finish/lwang-genomics-ngs_pipeline_sn-rna_seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/fastqc_raw.done`
- Representative outputs: `results/finish/fastqc_raw.done`
- Execution targets: `fastqc_raw`
- Downstream handoff: `trim`

## Guardrails
- Treat `results/finish/fastqc_raw.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/fastqc_raw.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `trim` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/fastqc_raw.done` exists and `trim` can proceed without re-running fastqc raw.
