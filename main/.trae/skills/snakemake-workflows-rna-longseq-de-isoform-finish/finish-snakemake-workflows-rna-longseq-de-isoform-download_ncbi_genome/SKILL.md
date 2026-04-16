---
name: finish-snakemake-workflows-rna-longseq-de-isoform-download_ncbi_genome
description: Use this skill when orchestrating the retained "download_ncbi_genome" step of the snakemake workflows rna longseq de isoform finish finish workflow. It keeps the download ncbi genome stage tied to upstream `bam_stats` and the downstream handoff to `download_ncbi_annotation`. It tracks completion via `results/finish/download_ncbi_genome.done`.
metadata:
  workflow_id: rna-longseq-de-isoform-finish
  workflow_name: snakemake workflows rna longseq de isoform finish
  step_id: download_ncbi_genome
  step_name: download ncbi genome
---

# Scope
Use this skill only for the `download_ncbi_genome` step in `rna-longseq-de-isoform-finish`.

## Orchestration
- Upstream requirements: `bam_stats`
- Step file: `finish/rna-longseq-de-isoform-finish/steps/download_ncbi_genome.smk`
- Config file: `finish/rna-longseq-de-isoform-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/download_ncbi_genome.done`
- Representative outputs: `results/finish/download_ncbi_genome.done`
- Execution targets: `download_ncbi_genome`
- Downstream handoff: `download_ncbi_annotation`

## Guardrails
- Treat `results/finish/download_ncbi_genome.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/download_ncbi_genome.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `download_ncbi_annotation` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/download_ncbi_genome.done` exists and `download_ncbi_annotation` can proceed without re-running download ncbi genome.
