---
name: finish-snakemake-workflows-rna-longseq-de-isoform-download_ensembl_annotation
description: Use this skill when orchestrating the retained "download_ensembl_annotation" step of the snakemake workflows rna longseq de isoform finish finish workflow. It keeps the download ensembl annotation stage tied to upstream `download_ensembl_genome` and the downstream handoff to `get_genome`. It tracks completion via `results/finish/download_ensembl_annotation.done`.
metadata:
  workflow_id: rna-longseq-de-isoform-finish
  workflow_name: snakemake workflows rna longseq de isoform finish
  step_id: download_ensembl_annotation
  step_name: download ensembl annotation
---

# Scope
Use this skill only for the `download_ensembl_annotation` step in `rna-longseq-de-isoform-finish`.

## Orchestration
- Upstream requirements: `download_ensembl_genome`
- Step file: `finish/rna-longseq-de-isoform-finish/steps/download_ensembl_annotation.smk`
- Config file: `finish/rna-longseq-de-isoform-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/download_ensembl_annotation.done`
- Representative outputs: `results/finish/download_ensembl_annotation.done`
- Execution targets: `download_ensembl_annotation`
- Downstream handoff: `get_genome`

## Guardrails
- Treat `results/finish/download_ensembl_annotation.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/download_ensembl_annotation.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `get_genome` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/download_ensembl_annotation.done` exists and `get_genome` can proceed without re-running download ensembl annotation.
