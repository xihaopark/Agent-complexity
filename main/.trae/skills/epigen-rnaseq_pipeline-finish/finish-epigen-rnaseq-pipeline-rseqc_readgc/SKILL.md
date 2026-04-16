---
name: finish-epigen-rnaseq-pipeline-rseqc_readgc
description: Use this skill when orchestrating the retained "rseqc_readgc" step of the epigen rnaseq_pipeline finish finish workflow. It keeps the rseqc readgc stage tied to upstream `rseqc_readdup` and the downstream handoff to `multiqc`. It tracks completion via `results/finish/rseqc_readgc.done`.
metadata:
  workflow_id: epigen-rnaseq_pipeline-finish
  workflow_name: epigen rnaseq_pipeline finish
  step_id: rseqc_readgc
  step_name: rseqc readgc
---

# Scope
Use this skill only for the `rseqc_readgc` step in `epigen-rnaseq_pipeline-finish`.

## Orchestration
- Upstream requirements: `rseqc_readdup`
- Step file: `finish/epigen-rnaseq_pipeline-finish/steps/rseqc_readgc.smk`
- Config file: `finish/epigen-rnaseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/rseqc_readgc.done`
- Representative outputs: `results/finish/rseqc_readgc.done`
- Execution targets: `rseqc_readgc`
- Downstream handoff: `multiqc`

## Guardrails
- Treat `results/finish/rseqc_readgc.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/rseqc_readgc.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `multiqc` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/rseqc_readgc.done` exists and `multiqc` can proceed without re-running rseqc readgc.
