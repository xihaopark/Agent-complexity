---
name: finish-epigen-rnaseq-pipeline-rseqc_infer
description: Use this skill when orchestrating the retained "rseqc_infer" step of the epigen rnaseq_pipeline finish finish workflow. It keeps the rseqc infer stage tied to upstream `rseqc_stat` and the downstream handoff to `rseqc_innerdis`. It tracks completion via `results/finish/rseqc_infer.done`.
metadata:
  workflow_id: epigen-rnaseq_pipeline-finish
  workflow_name: epigen rnaseq_pipeline finish
  step_id: rseqc_infer
  step_name: rseqc infer
---

# Scope
Use this skill only for the `rseqc_infer` step in `epigen-rnaseq_pipeline-finish`.

## Orchestration
- Upstream requirements: `rseqc_stat`
- Step file: `finish/epigen-rnaseq_pipeline-finish/steps/rseqc_infer.smk`
- Config file: `finish/epigen-rnaseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/rseqc_infer.done`
- Representative outputs: `results/finish/rseqc_infer.done`
- Execution targets: `rseqc_infer`
- Downstream handoff: `rseqc_innerdis`

## Guardrails
- Treat `results/finish/rseqc_infer.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/rseqc_infer.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `rseqc_innerdis` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/rseqc_infer.done` exists and `rseqc_innerdis` can proceed without re-running rseqc infer.
