---
name: finish-snakemake-workflows-rna-longseq-de-isoform-filter_reads
description: Use this skill when orchestrating the retained "filter_reads" step of the snakemake workflows rna longseq de isoform finish finish workflow. It keeps the filter reads stage tied to upstream `correct_transcriptome` and the downstream handoff to `build_minimap_index`. It tracks completion via `results/finish/filter_reads.done`.
metadata:
  workflow_id: rna-longseq-de-isoform-finish
  workflow_name: snakemake workflows rna longseq de isoform finish
  step_id: filter_reads
  step_name: filter reads
---

# Scope
Use this skill only for the `filter_reads` step in `rna-longseq-de-isoform-finish`.

## Orchestration
- Upstream requirements: `correct_transcriptome`
- Step file: `finish/rna-longseq-de-isoform-finish/steps/filter_reads.smk`
- Config file: `finish/rna-longseq-de-isoform-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/filter_reads.done`
- Representative outputs: `results/finish/filter_reads.done`
- Execution targets: `filter_reads`
- Downstream handoff: `build_minimap_index`

## Guardrails
- Treat `results/finish/filter_reads.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/filter_reads.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `build_minimap_index` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/filter_reads.done` exists and `build_minimap_index` can proceed without re-running filter reads.
