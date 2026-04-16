---
name: finish-snakemake-workflows-rna-seq-star-deseq2-multiqc
description: Use this skill when orchestrating the retained "multiqc" step of the snakemake workflows rna seq star deseq2 finish finish workflow. It keeps the multiqc stage tied to upstream `rseqc_readgc` and the downstream handoff to `star_align`. It tracks completion via `results/finish/multiqc.done`.
metadata:
  workflow_id: rna-seq-star-deseq2-finish
  workflow_name: snakemake workflows rna seq star deseq2 finish
  step_id: multiqc
  step_name: multiqc
---

# Scope
Use this skill only for the `multiqc` step in `rna-seq-star-deseq2-finish`.

## Orchestration
- Upstream requirements: `rseqc_readgc`
- Step file: `finish/rna-seq-star-deseq2-finish/steps/multiqc.smk`
- Config file: `finish/rna-seq-star-deseq2-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/multiqc.done`
- Representative outputs: `results/finish/multiqc.done`
- Execution targets: `multiqc`
- Downstream handoff: `star_align`

## Guardrails
- Treat `results/finish/multiqc.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/multiqc.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `star_align` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/multiqc.done` exists and `star_align` can proceed without re-running multiqc.
