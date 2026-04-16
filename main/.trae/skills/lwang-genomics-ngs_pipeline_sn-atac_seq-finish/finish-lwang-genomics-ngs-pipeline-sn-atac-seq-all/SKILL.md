---
name: finish-lwang-genomics-ngs-pipeline-sn-atac-seq-all
description: Use this skill when orchestrating the retained "all" step of the lwang genomics ngs_pipeline_sn atac_seq finish finish workflow. It keeps the all stage tied to upstream `multiqc`. It tracks completion via `results/finish/all.done`.
metadata:
  workflow_id: lwang-genomics-ngs_pipeline_sn-atac_seq-finish
  workflow_name: lwang genomics ngs_pipeline_sn atac_seq finish
  step_id: all
  step_name: all
---

# Scope
Use this skill only for the `all` step in `lwang-genomics-ngs_pipeline_sn-atac_seq-finish`.

## Orchestration
- Upstream requirements: `multiqc`
- Step file: `finish/lwang-genomics-ngs_pipeline_sn-atac_seq-finish/steps/all.smk`
- Config file: `finish/lwang-genomics-ngs_pipeline_sn-atac_seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/all.done`
- Representative outputs: `results/finish/all.done`
- Execution targets: `all`
- Downstream handoff: none

## Guardrails
- Treat `results/finish/all.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/all.smk` so the step remains separable and replayable inside the finish workflow.

## Done Criteria
Mark this step complete only when `results/finish/all.done` exists and matches the intended step boundary.
