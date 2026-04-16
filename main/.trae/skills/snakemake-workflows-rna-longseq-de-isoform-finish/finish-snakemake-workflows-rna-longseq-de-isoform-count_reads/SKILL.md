---
name: finish-snakemake-workflows-rna-longseq-de-isoform-count_reads
description: Use this skill when orchestrating the retained "count_reads" step of the snakemake workflows rna longseq de isoform finish finish workflow. It keeps the count reads stage tied to upstream `bam_index` and the downstream handoff to `merge_read_counts`. It tracks completion via `results/finish/count_reads.done`.
metadata:
  workflow_id: rna-longseq-de-isoform-finish
  workflow_name: snakemake workflows rna longseq de isoform finish
  step_id: count_reads
  step_name: count reads
---

# Scope
Use this skill only for the `count_reads` step in `rna-longseq-de-isoform-finish`.

## Orchestration
- Upstream requirements: `bam_index`
- Step file: `finish/rna-longseq-de-isoform-finish/steps/count_reads.smk`
- Config file: `finish/rna-longseq-de-isoform-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/count_reads.done`
- Representative outputs: `results/finish/count_reads.done`
- Execution targets: `count_reads`
- Downstream handoff: `merge_read_counts`

## Guardrails
- Treat `results/finish/count_reads.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/count_reads.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `merge_read_counts` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/count_reads.done` exists and `merge_read_counts` can proceed without re-running count reads.
