---
name: finish-saidmlonji-rnaseq-pipeline-gene_counting
description: Use this skill when orchestrating the retained "gene_counting" step of the saidmlonji rnaseq_pipeline finish finish workflow. It keeps the Gene Counting stage tied to upstream `alignment_qc` and the downstream handoff to `deseq2_analysis`. It tracks completion via `results/finish/gene_counting.done`.
metadata:
  workflow_id: saidmlonji-rnaseq_pipeline-finish
  workflow_name: saidmlonji rnaseq_pipeline finish
  step_id: gene_counting
  step_name: Gene Counting
---

# Scope
Use this skill only for the `gene_counting` step in `saidmlonji-rnaseq_pipeline-finish`.

## Orchestration
- Upstream requirements: `alignment_qc`
- Step file: `finish/saidmlonji-rnaseq_pipeline-finish/steps/gene_counting.smk`
- Config file: `finish/saidmlonji-rnaseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/gene_counting.done`
- Representative outputs: `results/finish/gene_counting.done`
- Execution targets: `gene_counting`
- Downstream handoff: `deseq2_analysis`

## Guardrails
- Treat `results/finish/gene_counting.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/gene_counting.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `deseq2_analysis` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/gene_counting.done` exists and `deseq2_analysis` can proceed without re-running Gene Counting.
