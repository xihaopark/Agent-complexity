---
name: finish-snakemake-workflows-rna-longseq-de-isoform-merge_read_counts
description: Use this skill when orchestrating the retained "merge_read_counts" step of the snakemake workflows rna longseq de isoform finish finish workflow. It keeps the merge read counts stage tied to upstream `count_reads` and the downstream handoff to `transcriptid_to_gene`. It tracks completion via `results/finish/merge_read_counts.done`.
metadata:
  workflow_id: rna-longseq-de-isoform-finish
  workflow_name: snakemake workflows rna longseq de isoform finish
  step_id: merge_read_counts
  step_name: merge read counts
---

# Scope
Use this skill only for the `merge_read_counts` step in `rna-longseq-de-isoform-finish`.

## Orchestration
- Upstream requirements: `count_reads`
- Step file: `finish/rna-longseq-de-isoform-finish/steps/merge_read_counts.smk`
- Config file: `finish/rna-longseq-de-isoform-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/merge_read_counts.done`
- Representative outputs: `results/finish/merge_read_counts.done`
- Execution targets: `merge_read_counts`
- Downstream handoff: `transcriptid_to_gene`

## Guardrails
- Treat `results/finish/merge_read_counts.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/merge_read_counts.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `transcriptid_to_gene` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/merge_read_counts.done` exists and `transcriptid_to_gene` can proceed without re-running merge read counts.
