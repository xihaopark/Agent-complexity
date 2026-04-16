---
name: finish-snakemake-workflows-rna-longseq-de-isoform-bam_sort
description: Use this skill when orchestrating the retained "bam_sort" step of the snakemake workflows rna longseq de isoform finish finish workflow. It keeps the bam sort stage tied to upstream `sam_to_bam` and the downstream handoff to `bam_index`. It tracks completion via `results/finish/bam_sort.done`.
metadata:
  workflow_id: rna-longseq-de-isoform-finish
  workflow_name: snakemake workflows rna longseq de isoform finish
  step_id: bam_sort
  step_name: bam sort
---

# Scope
Use this skill only for the `bam_sort` step in `rna-longseq-de-isoform-finish`.

## Orchestration
- Upstream requirements: `sam_to_bam`
- Step file: `finish/rna-longseq-de-isoform-finish/steps/bam_sort.smk`
- Config file: `finish/rna-longseq-de-isoform-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/bam_sort.done`
- Representative outputs: `results/finish/bam_sort.done`
- Execution targets: `bam_sort`
- Downstream handoff: `bam_index`

## Guardrails
- Treat `results/finish/bam_sort.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/bam_sort.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `bam_index` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/bam_sort.done` exists and `bam_index` can proceed without re-running bam sort.
