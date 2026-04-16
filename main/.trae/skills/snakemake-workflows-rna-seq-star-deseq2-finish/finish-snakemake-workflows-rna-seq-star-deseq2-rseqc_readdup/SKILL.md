---
name: finish-snakemake-workflows-rna-seq-star-deseq2-rseqc_readdup
description: Use this skill when orchestrating the retained "rseqc_readdup" step of the snakemake workflows rna seq star deseq2 finish finish workflow. It keeps the rseqc readdup stage tied to upstream `rseqc_readdis` and the downstream handoff to `rseqc_readgc`. It tracks completion via `results/finish/rseqc_readdup.done`.
metadata:
  workflow_id: rna-seq-star-deseq2-finish
  workflow_name: snakemake workflows rna seq star deseq2 finish
  step_id: rseqc_readdup
  step_name: rseqc readdup
---

# Scope
Use this skill only for the `rseqc_readdup` step in `rna-seq-star-deseq2-finish`.

## Orchestration
- Upstream requirements: `rseqc_readdis`
- Step file: `finish/rna-seq-star-deseq2-finish/steps/rseqc_readdup.smk`
- Config file: `finish/rna-seq-star-deseq2-finish/config_basic/config.yaml`
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
