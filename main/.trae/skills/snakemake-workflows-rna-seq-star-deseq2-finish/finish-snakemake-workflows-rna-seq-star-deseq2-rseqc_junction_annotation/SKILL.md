---
name: finish-snakemake-workflows-rna-seq-star-deseq2-rseqc_junction_annotation
description: Use this skill when orchestrating the retained "rseqc_junction_annotation" step of the snakemake workflows rna seq star deseq2 finish finish workflow. It keeps the rseqc junction annotation stage tied to upstream `rseqc_gtf2bed` and the downstream handoff to `rseqc_junction_saturation`. It tracks completion via `results/finish/rseqc_junction_annotation.done`.
metadata:
  workflow_id: rna-seq-star-deseq2-finish
  workflow_name: snakemake workflows rna seq star deseq2 finish
  step_id: rseqc_junction_annotation
  step_name: rseqc junction annotation
---

# Scope
Use this skill only for the `rseqc_junction_annotation` step in `rna-seq-star-deseq2-finish`.

## Orchestration
- Upstream requirements: `rseqc_gtf2bed`
- Step file: `finish/rna-seq-star-deseq2-finish/steps/rseqc_junction_annotation.smk`
- Config file: `finish/rna-seq-star-deseq2-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/rseqc_junction_annotation.done`
- Representative outputs: `results/finish/rseqc_junction_annotation.done`
- Execution targets: `rseqc_junction_annotation`
- Downstream handoff: `rseqc_junction_saturation`

## Guardrails
- Treat `results/finish/rseqc_junction_annotation.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/rseqc_junction_annotation.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `rseqc_junction_saturation` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/rseqc_junction_annotation.done` exists and `rseqc_junction_saturation` can proceed without re-running rseqc junction annotation.
