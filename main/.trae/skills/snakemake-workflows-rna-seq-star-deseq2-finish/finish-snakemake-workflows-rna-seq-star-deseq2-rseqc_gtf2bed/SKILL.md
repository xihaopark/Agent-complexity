---
name: finish-snakemake-workflows-rna-seq-star-deseq2-rseqc_gtf2bed
description: Use this skill when orchestrating the retained "rseqc_gtf2bed" step of the snakemake workflows rna seq star deseq2 finish finish workflow. It keeps the rseqc gtf2bed stage tied to upstream `fastp_pe` and the downstream handoff to `rseqc_junction_annotation`. It tracks completion via `results/finish/rseqc_gtf2bed.done`.
metadata:
  workflow_id: rna-seq-star-deseq2-finish
  workflow_name: snakemake workflows rna seq star deseq2 finish
  step_id: rseqc_gtf2bed
  step_name: rseqc gtf2bed
---

# Scope
Use this skill only for the `rseqc_gtf2bed` step in `rna-seq-star-deseq2-finish`.

## Orchestration
- Upstream requirements: `fastp_pe`
- Step file: `finish/rna-seq-star-deseq2-finish/steps/rseqc_gtf2bed.smk`
- Config file: `finish/rna-seq-star-deseq2-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/rseqc_gtf2bed.done`
- Representative outputs: `results/finish/rseqc_gtf2bed.done`
- Execution targets: `rseqc_gtf2bed`
- Downstream handoff: `rseqc_junction_annotation`

## Guardrails
- Treat `results/finish/rseqc_gtf2bed.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/rseqc_gtf2bed.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `rseqc_junction_annotation` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/rseqc_gtf2bed.done` exists and `rseqc_junction_annotation` can proceed without re-running rseqc gtf2bed.
