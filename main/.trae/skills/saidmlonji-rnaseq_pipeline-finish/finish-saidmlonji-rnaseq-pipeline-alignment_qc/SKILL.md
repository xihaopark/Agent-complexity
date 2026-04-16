---
name: finish-saidmlonji-rnaseq-pipeline-alignment_qc
description: Use this skill when orchestrating the retained "alignment_qc" step of the saidmlonji rnaseq_pipeline finish finish workflow. It keeps the Alignment QC stage and the downstream handoff to `gene_counting`. It tracks completion via `results/finish/alignment_qc.done`.
metadata:
  workflow_id: saidmlonji-rnaseq_pipeline-finish
  workflow_name: saidmlonji rnaseq_pipeline finish
  step_id: alignment_qc
  step_name: Alignment QC
---

# Scope
Use this skill only for the `alignment_qc` step in `saidmlonji-rnaseq_pipeline-finish`.

## Orchestration
- Upstream requirements: none
- Step file: `finish/saidmlonji-rnaseq_pipeline-finish/steps/alignment_qc.smk`
- Config file: `finish/saidmlonji-rnaseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/alignment_qc.done`
- Representative outputs: `results/finish/alignment_qc.done`
- Execution targets: `alignment_qc`
- Downstream handoff: `gene_counting`

## Guardrails
- Treat `results/finish/alignment_qc.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/alignment_qc.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `gene_counting` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/alignment_qc.done` exists and `gene_counting` can proceed without re-running Alignment QC.
