---
name: finish-lwang-genomics-ngs-pipeline-sn-rna-seq-count_gene
description: Use this skill when orchestrating the retained "count_gene" step of the lwang genomics ngs_pipeline_sn rna_seq finish finish workflow. It keeps the count gene stage tied to upstream `convert_bw` and the downstream handoff to `qualimap_qc`. It tracks completion via `results/finish/count_gene.done`.
metadata:
  workflow_id: lwang-genomics-ngs_pipeline_sn-rna_seq-finish
  workflow_name: lwang genomics ngs_pipeline_sn rna_seq finish
  step_id: count_gene
  step_name: count gene
---

# Scope
Use this skill only for the `count_gene` step in `lwang-genomics-ngs_pipeline_sn-rna_seq-finish`.

## Orchestration
- Upstream requirements: `convert_bw`
- Step file: `finish/lwang-genomics-ngs_pipeline_sn-rna_seq-finish/steps/count_gene.smk`
- Config file: `finish/lwang-genomics-ngs_pipeline_sn-rna_seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/count_gene.done`
- Representative outputs: `results/finish/count_gene.done`
- Execution targets: `count_gene`
- Downstream handoff: `qualimap_qc`

## Guardrails
- Treat `results/finish/count_gene.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/count_gene.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `qualimap_qc` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/count_gene.done` exists and `qualimap_qc` can proceed without re-running count gene.
