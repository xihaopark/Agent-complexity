---
name: finish-snakemake-workflows-rna-longseq-de-isoform-bam_index
description: Use this skill when orchestrating the retained "bam_index" step of the snakemake workflows rna longseq de isoform finish finish workflow. It keeps the bam index stage tied to upstream `bam_sort` and the downstream handoff to `count_reads`. It tracks completion via `results/finish/bam_index.done`.
metadata:
  workflow_id: rna-longseq-de-isoform-finish
  workflow_name: snakemake workflows rna longseq de isoform finish
  step_id: bam_index
  step_name: bam index
---

# Scope
Use this skill only for the `bam_index` step in `rna-longseq-de-isoform-finish`.

## Orchestration
- Upstream requirements: `bam_sort`
- Step file: `finish/rna-longseq-de-isoform-finish/steps/bam_index.smk`
- Config file: `finish/rna-longseq-de-isoform-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/bam_index.done`
- Representative outputs: `results/finish/bam_index.done`
- Execution targets: `bam_index`
- Downstream handoff: `count_reads`

## Guardrails
- Treat `results/finish/bam_index.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/bam_index.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `count_reads` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/bam_index.done` exists and `count_reads` can proceed without re-running bam index.
