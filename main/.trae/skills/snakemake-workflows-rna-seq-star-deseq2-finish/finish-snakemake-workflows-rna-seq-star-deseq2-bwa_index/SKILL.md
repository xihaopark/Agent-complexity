---
name: finish-snakemake-workflows-rna-seq-star-deseq2-bwa_index
description: Use this skill when orchestrating the retained "bwa_index" step of the snakemake workflows rna seq star deseq2 finish finish workflow. It keeps the bwa index stage tied to upstream `genome_faidx` and the downstream handoff to `star_index`. It tracks completion via `results/finish/bwa_index.done`.
metadata:
  workflow_id: rna-seq-star-deseq2-finish
  workflow_name: snakemake workflows rna seq star deseq2 finish
  step_id: bwa_index
  step_name: bwa index
---

# Scope
Use this skill only for the `bwa_index` step in `rna-seq-star-deseq2-finish`.

## Orchestration
- Upstream requirements: `genome_faidx`
- Step file: `finish/rna-seq-star-deseq2-finish/steps/bwa_index.smk`
- Config file: `finish/rna-seq-star-deseq2-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/bwa_index.done`
- Representative outputs: `results/finish/bwa_index.done`
- Execution targets: `bwa_index`
- Downstream handoff: `star_index`

## Guardrails
- Treat `results/finish/bwa_index.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/bwa_index.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `star_index` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/bwa_index.done` exists and `star_index` can proceed without re-running bwa index.
