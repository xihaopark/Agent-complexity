---
name: finish-epigen-rnaseq-pipeline-rseqc_readdup
description: Use this skill when orchestrating the retained "rseqc_readdup" step of the epigen rnaseq_pipeline finish finish workflow. It keeps the rseqc readdup stage tied to upstream `rseqc_readdis` and the downstream handoff to `rseqc_readgc`. It tracks completion via `results/finish/rseqc_readdup.done`.
metadata:
  workflow_id: epigen-rnaseq_pipeline-finish
  workflow_name: epigen rnaseq_pipeline finish
  step_id: rseqc_readdup
  step_name: rseqc readdup
---

# Scope
Use this skill only for the `rseqc_readdup` step in `epigen-rnaseq_pipeline-finish`.

## Orchestration
- Upstream requirements: `rseqc_readdis`
- Step file: `finish/epigen-rnaseq_pipeline-finish/steps/rseqc_readdup.smk`
- Config file: `finish/epigen-rnaseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/rseqc_readdup.done`
- Representative outputs: `results/finish/rseqc_readdup.done`
- Execution targets: `rseqc_readdup`
- Downstream handoff: `rseqc_readgc`

## Guardrails
- Treat `results/finish/rseqc_readdup.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/rseqc_readdup.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `rseqc_readgc` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/rseqc_readdup.done` exists and `rseqc_readgc` can proceed without re-running rseqc readdup.
