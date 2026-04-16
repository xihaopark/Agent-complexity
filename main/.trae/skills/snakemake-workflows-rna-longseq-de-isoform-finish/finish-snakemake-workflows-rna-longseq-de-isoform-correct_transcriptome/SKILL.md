---
name: finish-snakemake-workflows-rna-longseq-de-isoform-correct_transcriptome
description: Use this skill when orchestrating the retained "correct_transcriptome" step of the snakemake workflows rna longseq de isoform finish finish workflow. It keeps the correct transcriptome stage tied to upstream `genome_to_transcriptome` and the downstream handoff to `filter_reads`. It tracks completion via `results/finish/correct_transcriptome.done`.
metadata:
  workflow_id: rna-longseq-de-isoform-finish
  workflow_name: snakemake workflows rna longseq de isoform finish
  step_id: correct_transcriptome
  step_name: correct transcriptome
---

# Scope
Use this skill only for the `correct_transcriptome` step in `rna-longseq-de-isoform-finish`.

## Orchestration
- Upstream requirements: `genome_to_transcriptome`
- Step file: `finish/rna-longseq-de-isoform-finish/steps/correct_transcriptome.smk`
- Config file: `finish/rna-longseq-de-isoform-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/correct_transcriptome.done`
- Representative outputs: `results/finish/correct_transcriptome.done`
- Execution targets: `correct_transcriptome`
- Downstream handoff: `filter_reads`

## Guardrails
- Treat `results/finish/correct_transcriptome.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/correct_transcriptome.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `filter_reads` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/correct_transcriptome.done` exists and `filter_reads` can proceed without re-running correct transcriptome.
