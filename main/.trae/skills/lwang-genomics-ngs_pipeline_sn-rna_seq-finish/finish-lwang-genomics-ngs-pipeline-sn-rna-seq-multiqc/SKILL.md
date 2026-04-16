---
name: finish-lwang-genomics-ngs-pipeline-sn-rna-seq-multiqc
description: Use this skill when orchestrating the retained "multiqc" step of the lwang genomics ngs_pipeline_sn rna_seq finish finish workflow. It keeps the multiqc stage tied to upstream `qualimap_qc` and the downstream handoff to `all`. It tracks completion via `results/finish/multiqc.done`.
metadata:
  workflow_id: lwang-genomics-ngs_pipeline_sn-rna_seq-finish
  workflow_name: lwang genomics ngs_pipeline_sn rna_seq finish
  step_id: multiqc
  step_name: multiqc
---

# Scope
Use this skill only for the `multiqc` step in `lwang-genomics-ngs_pipeline_sn-rna_seq-finish`.

## Orchestration
- Upstream requirements: `qualimap_qc`
- Step file: `finish/lwang-genomics-ngs_pipeline_sn-rna_seq-finish/steps/multiqc.smk`
- Config file: `finish/lwang-genomics-ngs_pipeline_sn-rna_seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/multiqc.done`
- Representative outputs: `results/finish/multiqc.done`
- Execution targets: `multiqc`
- Downstream handoff: `all`

## Guardrails
- Treat `results/finish/multiqc.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/multiqc.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `all` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/multiqc.done` exists and `all` can proceed without re-running multiqc.
