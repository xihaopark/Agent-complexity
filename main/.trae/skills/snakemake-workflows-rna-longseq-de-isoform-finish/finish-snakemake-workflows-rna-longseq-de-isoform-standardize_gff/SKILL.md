---
name: finish-snakemake-workflows-rna-longseq-de-isoform-standardize_gff
description: Use this skill when orchestrating the retained "standardize_gff" step of the snakemake workflows rna longseq de isoform finish finish workflow. It keeps the standardize gff stage tied to upstream `get_annotation` and the downstream handoff to `genome_to_transcriptome`. It tracks completion via `results/finish/standardize_gff.done`.
metadata:
  workflow_id: rna-longseq-de-isoform-finish
  workflow_name: snakemake workflows rna longseq de isoform finish
  step_id: standardize_gff
  step_name: standardize gff
---

# Scope
Use this skill only for the `standardize_gff` step in `rna-longseq-de-isoform-finish`.

## Orchestration
- Upstream requirements: `get_annotation`
- Step file: `finish/rna-longseq-de-isoform-finish/steps/standardize_gff.smk`
- Config file: `finish/rna-longseq-de-isoform-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/standardize_gff.done`
- Representative outputs: `results/finish/standardize_gff.done`
- Execution targets: `standardize_gff`
- Downstream handoff: `genome_to_transcriptome`

## Guardrails
- Treat `results/finish/standardize_gff.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/standardize_gff.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `genome_to_transcriptome` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/standardize_gff.done` exists and `genome_to_transcriptome` can proceed without re-running standardize gff.
