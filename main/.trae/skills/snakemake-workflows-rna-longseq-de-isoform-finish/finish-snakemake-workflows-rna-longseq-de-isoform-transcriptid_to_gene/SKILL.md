---
name: finish-snakemake-workflows-rna-longseq-de-isoform-transcriptid_to_gene
description: Use this skill when orchestrating the retained "transcriptid_to_gene" step of the snakemake workflows rna longseq de isoform finish finish workflow. It keeps the transcriptid to gene stage tied to upstream `merge_read_counts` and the downstream handoff to `deseq2_init`. It tracks completion via `results/finish/transcriptid_to_gene.done`.
metadata:
  workflow_id: rna-longseq-de-isoform-finish
  workflow_name: snakemake workflows rna longseq de isoform finish
  step_id: transcriptid_to_gene
  step_name: transcriptid to gene
---

# Scope
Use this skill only for the `transcriptid_to_gene` step in `rna-longseq-de-isoform-finish`.

## Orchestration
- Upstream requirements: `merge_read_counts`
- Step file: `finish/rna-longseq-de-isoform-finish/steps/transcriptid_to_gene.smk`
- Config file: `finish/rna-longseq-de-isoform-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/transcriptid_to_gene.done`
- Representative outputs: `results/finish/transcriptid_to_gene.done`
- Execution targets: `transcriptid_to_gene`
- Downstream handoff: `deseq2_init`

## Guardrails
- Treat `results/finish/transcriptid_to_gene.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/transcriptid_to_gene.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `deseq2_init` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/transcriptid_to_gene.done` exists and `deseq2_init` can proceed without re-running transcriptid to gene.
