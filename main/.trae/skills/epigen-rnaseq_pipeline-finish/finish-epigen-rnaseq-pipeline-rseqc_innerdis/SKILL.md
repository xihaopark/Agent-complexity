---
name: finish-epigen-rnaseq-pipeline-rseqc_innerdis
description: Use this skill when orchestrating the retained "rseqc_innerdis" step of the epigen rnaseq_pipeline finish finish workflow. It keeps the rseqc innerdis stage tied to upstream `rseqc_infer` and the downstream handoff to `rseqc_readdis`. It tracks completion via `results/finish/rseqc_innerdis.done`.
metadata:
  workflow_id: epigen-rnaseq_pipeline-finish
  workflow_name: epigen rnaseq_pipeline finish
  step_id: rseqc_innerdis
  step_name: rseqc innerdis
---

# Scope
Use this skill only for the `rseqc_innerdis` step in `epigen-rnaseq_pipeline-finish`.

## Orchestration
- Upstream requirements: `rseqc_infer`
- Step file: `finish/epigen-rnaseq_pipeline-finish/steps/rseqc_innerdis.smk`
- Config file: `finish/epigen-rnaseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/rseqc_innerdis.done`
- Representative outputs: `results/finish/rseqc_innerdis.done`
- Execution targets: `rseqc_innerdis`
- Downstream handoff: `rseqc_readdis`

## Guardrails
- Treat `results/finish/rseqc_innerdis.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/rseqc_innerdis.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `rseqc_readdis` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/rseqc_innerdis.done` exists and `rseqc_readdis` can proceed without re-running rseqc innerdis.
