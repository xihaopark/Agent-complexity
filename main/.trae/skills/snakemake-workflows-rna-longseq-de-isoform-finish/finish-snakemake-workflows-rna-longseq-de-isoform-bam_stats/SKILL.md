---
name: finish-snakemake-workflows-rna-longseq-de-isoform-bam_stats
description: Use this skill when orchestrating the retained "bam_stats" step of the snakemake workflows rna longseq de isoform finish finish workflow. It keeps the bam stats stage tied to upstream `alignment_qa_report` and the downstream handoff to `download_ncbi_genome`. It tracks completion via `results/finish/bam_stats.done`.
metadata:
  workflow_id: rna-longseq-de-isoform-finish
  workflow_name: snakemake workflows rna longseq de isoform finish
  step_id: bam_stats
  step_name: bam stats
---

# Scope
Use this skill only for the `bam_stats` step in `rna-longseq-de-isoform-finish`.

## Orchestration
- Upstream requirements: `alignment_qa_report`
- Step file: `finish/rna-longseq-de-isoform-finish/steps/bam_stats.smk`
- Config file: `finish/rna-longseq-de-isoform-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/bam_stats.done`
- Representative outputs: `results/finish/bam_stats.done`
- Execution targets: `bam_stats`
- Downstream handoff: `download_ncbi_genome`

## Guardrails
- Treat `results/finish/bam_stats.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/bam_stats.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `download_ncbi_genome` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/bam_stats.done` exists and `download_ncbi_genome` can proceed without re-running bam stats.
