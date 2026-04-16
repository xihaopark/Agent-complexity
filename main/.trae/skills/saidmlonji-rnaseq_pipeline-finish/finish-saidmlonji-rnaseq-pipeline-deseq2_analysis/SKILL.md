---
name: finish-saidmlonji-rnaseq-pipeline-deseq2_analysis
description: Use this skill when orchestrating the retained "deseq2_analysis" step of the saidmlonji rnaseq_pipeline finish finish workflow. It keeps the DESeq2 Analysis stage tied to upstream `gene_counting`. It tracks completion via `results/finish/deseq2_analysis.done`.
metadata:
  workflow_id: saidmlonji-rnaseq_pipeline-finish
  workflow_name: saidmlonji rnaseq_pipeline finish
  step_id: deseq2_analysis
  step_name: DESeq2 Analysis
---

# Scope
Use this skill only for the `deseq2_analysis` step in `saidmlonji-rnaseq_pipeline-finish`.

## Orchestration
- Upstream requirements: `gene_counting`
- Step file: `finish/saidmlonji-rnaseq_pipeline-finish/steps/deseq2_analysis.smk`
- Config file: `finish/saidmlonji-rnaseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/deseq2_analysis.done`
- Representative outputs: `results/finish/deseq2_analysis.done`
- Execution targets: `deseq2_analysis`
- Downstream handoff: none

## Guardrails
- Treat `results/finish/deseq2_analysis.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/deseq2_analysis.smk` so the step remains separable and replayable inside the finish workflow.

## Done Criteria
Mark this step complete only when `results/finish/deseq2_analysis.done` exists and matches the intended step boundary.
