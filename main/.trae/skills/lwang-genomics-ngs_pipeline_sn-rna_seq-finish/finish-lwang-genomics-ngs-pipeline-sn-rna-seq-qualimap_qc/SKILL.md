---
name: finish-lwang-genomics-ngs-pipeline-sn-rna-seq-qualimap_qc
description: Use this skill when orchestrating the retained "qualimap_qc" step of the lwang genomics ngs_pipeline_sn rna_seq finish finish workflow. It keeps the qualimap qc stage tied to upstream `count_gene` and the downstream handoff to `multiqc`. It tracks completion via `results/finish/qualimap_qc.done`.
metadata:
  workflow_id: lwang-genomics-ngs_pipeline_sn-rna_seq-finish
  workflow_name: lwang genomics ngs_pipeline_sn rna_seq finish
  step_id: qualimap_qc
  step_name: qualimap qc
---

# Scope
Use this skill only for the `qualimap_qc` step in `lwang-genomics-ngs_pipeline_sn-rna_seq-finish`.

## Orchestration
- Upstream requirements: `count_gene`
- Step file: `finish/lwang-genomics-ngs_pipeline_sn-rna_seq-finish/steps/qualimap_qc.smk`
- Config file: `finish/lwang-genomics-ngs_pipeline_sn-rna_seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/qualimap_qc.done`
- Representative outputs: `results/finish/qualimap_qc.done`
- Execution targets: `qualimap_qc`
- Downstream handoff: `multiqc`

## Guardrails
- Treat `results/finish/qualimap_qc.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/qualimap_qc.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `multiqc` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/qualimap_qc.done` exists and `multiqc` can proceed without re-running qualimap qc.
