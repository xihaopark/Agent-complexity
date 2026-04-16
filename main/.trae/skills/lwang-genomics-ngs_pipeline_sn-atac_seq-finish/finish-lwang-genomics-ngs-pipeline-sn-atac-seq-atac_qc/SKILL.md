---
name: finish-lwang-genomics-ngs-pipeline-sn-atac-seq-atac_qc
description: Use this skill when orchestrating the retained "atac_qc" step of the lwang genomics ngs_pipeline_sn atac_seq finish finish workflow. It keeps the atac qc stage tied to upstream `call_peaks` and the downstream handoff to `multiqc`. It tracks completion via `results/finish/atac_qc.done`.
metadata:
  workflow_id: lwang-genomics-ngs_pipeline_sn-atac_seq-finish
  workflow_name: lwang genomics ngs_pipeline_sn atac_seq finish
  step_id: atac_qc
  step_name: atac qc
---

# Scope
Use this skill only for the `atac_qc` step in `lwang-genomics-ngs_pipeline_sn-atac_seq-finish`.

## Orchestration
- Upstream requirements: `call_peaks`
- Step file: `finish/lwang-genomics-ngs_pipeline_sn-atac_seq-finish/steps/atac_qc.smk`
- Config file: `finish/lwang-genomics-ngs_pipeline_sn-atac_seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/atac_qc.done`
- Representative outputs: `results/finish/atac_qc.done`
- Execution targets: `atac_qc`
- Downstream handoff: `multiqc`

## Guardrails
- Treat `results/finish/atac_qc.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/atac_qc.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `multiqc` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/atac_qc.done` exists and `multiqc` can proceed without re-running atac qc.
