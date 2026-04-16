---
name: finish-snakemake-workflows-rna-longseq-de-isoform-download_ncbi_annotation
description: Use this skill when orchestrating the retained "download_ncbi_annotation" step of the snakemake workflows rna longseq de isoform finish finish workflow. It keeps the download ncbi annotation stage tied to upstream `download_ncbi_genome` and the downstream handoff to `download_ensembl_genome`. It tracks completion via `results/finish/download_ncbi_annotation.done`.
metadata:
  workflow_id: rna-longseq-de-isoform-finish
  workflow_name: snakemake workflows rna longseq de isoform finish
  step_id: download_ncbi_annotation
  step_name: download ncbi annotation
---

# Scope
Use this skill only for the `download_ncbi_annotation` step in `rna-longseq-de-isoform-finish`.

## Orchestration
- Upstream requirements: `download_ncbi_genome`
- Step file: `finish/rna-longseq-de-isoform-finish/steps/download_ncbi_annotation.smk`
- Config file: `finish/rna-longseq-de-isoform-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/download_ncbi_annotation.done`
- Representative outputs: `results/finish/download_ncbi_annotation.done`
- Execution targets: `download_ncbi_annotation`
- Downstream handoff: `download_ensembl_genome`

## Guardrails
- Treat `results/finish/download_ncbi_annotation.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/download_ncbi_annotation.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `download_ensembl_genome` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/download_ncbi_annotation.done` exists and `download_ensembl_genome` can proceed without re-running download ncbi annotation.
