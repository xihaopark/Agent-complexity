---
name: finish-snakemake-workflows-rna-seq-star-deseq2-star_align
description: Use this skill when orchestrating the retained "star_align" step of the snakemake workflows rna seq star deseq2 finish finish workflow. It keeps the star align stage tied to upstream `multiqc` and the downstream handoff to `count_matrix`. It tracks completion via `results/finish/star_align.done`.
metadata:
  workflow_id: rna-seq-star-deseq2-finish
  workflow_name: snakemake workflows rna seq star deseq2 finish
  step_id: star_align
  step_name: star align
---

# Scope
Use this skill only for the `star_align` step in `rna-seq-star-deseq2-finish`.

## Orchestration
- Upstream requirements: `multiqc`
- Step file: `finish/rna-seq-star-deseq2-finish/steps/star_align.smk`
- Config file: `finish/rna-seq-star-deseq2-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/star_align.done`
- Representative outputs: `results/finish/star_align.done`
- Execution targets: `star_align`
- Downstream handoff: `count_matrix`

## Guardrails
- Treat `results/finish/star_align.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/star_align.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `count_matrix` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/star_align.done` exists and `count_matrix` can proceed without re-running star align.
