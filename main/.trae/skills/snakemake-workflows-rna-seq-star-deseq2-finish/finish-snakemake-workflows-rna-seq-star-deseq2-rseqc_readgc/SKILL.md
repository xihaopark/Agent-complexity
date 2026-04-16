---
name: finish-snakemake-workflows-rna-seq-star-deseq2-rseqc_readgc
description: Use this skill when orchestrating the retained "rseqc_readgc" step of the snakemake workflows rna seq star deseq2 finish finish workflow. It keeps the rseqc readgc stage tied to upstream `rseqc_readdup` and the downstream handoff to `multiqc`. It tracks completion via `results/finish/rseqc_readgc.done`.
metadata:
  workflow_id: rna-seq-star-deseq2-finish
  workflow_name: snakemake workflows rna seq star deseq2 finish
  step_id: rseqc_readgc
  step_name: rseqc readgc
---

# Scope
Use this skill only for the `rseqc_readgc` step in `rna-seq-star-deseq2-finish`.

## Orchestration
- Upstream requirements: `rseqc_readdup`
- Step file: `finish/rna-seq-star-deseq2-finish/steps/rseqc_readgc.smk`
- Config file: `finish/rna-seq-star-deseq2-finish/config_basic/config.yaml`
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
