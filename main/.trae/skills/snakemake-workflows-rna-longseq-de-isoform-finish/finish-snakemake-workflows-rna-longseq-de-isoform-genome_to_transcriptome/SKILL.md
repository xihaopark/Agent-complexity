---
name: finish-snakemake-workflows-rna-longseq-de-isoform-genome_to_transcriptome
description: Use this skill when orchestrating the retained "genome_to_transcriptome" step of the snakemake workflows rna longseq de isoform finish finish workflow. It keeps the genome to transcriptome stage tied to upstream `standardize_gff` and the downstream handoff to `correct_transcriptome`. It tracks completion via `results/finish/genome_to_transcriptome.done`.
metadata:
  workflow_id: rna-longseq-de-isoform-finish
  workflow_name: snakemake workflows rna longseq de isoform finish
  step_id: genome_to_transcriptome
  step_name: genome to transcriptome
---

# Scope
Use this skill only for the `genome_to_transcriptome` step in `rna-longseq-de-isoform-finish`.

## Orchestration
- Upstream requirements: `standardize_gff`
- Step file: `finish/rna-longseq-de-isoform-finish/steps/genome_to_transcriptome.smk`
- Config file: `finish/rna-longseq-de-isoform-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/genome_to_transcriptome.done`
- Representative outputs: `results/finish/genome_to_transcriptome.done`
- Execution targets: `genome_to_transcriptome`
- Downstream handoff: `correct_transcriptome`

## Guardrails
- Treat `results/finish/genome_to_transcriptome.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/genome_to_transcriptome.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `correct_transcriptome` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/genome_to_transcriptome.done` exists and `correct_transcriptome` can proceed without re-running genome to transcriptome.
