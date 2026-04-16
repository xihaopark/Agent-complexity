---
name: finish-snakemake-workflows-rna-longseq-de-isoform-alignment_qa_report
description: Use this skill when orchestrating the retained "alignment_qa_report" step of the snakemake workflows rna longseq de isoform finish finish workflow. It keeps the alignment qa report stage tied to upstream `alignment_qa` and the downstream handoff to `bam_stats`. It tracks completion via `results/finish/alignment_qa_report.done`.
metadata:
  workflow_id: rna-longseq-de-isoform-finish
  workflow_name: snakemake workflows rna longseq de isoform finish
  step_id: alignment_qa_report
  step_name: alignment qa report
---

# Scope
Use this skill only for the `alignment_qa_report` step in `rna-longseq-de-isoform-finish`.

## Orchestration
- Upstream requirements: `alignment_qa`
- Step file: `finish/rna-longseq-de-isoform-finish/steps/alignment_qa_report.smk`
- Config file: `finish/rna-longseq-de-isoform-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/alignment_qa_report.done`
- Representative outputs: `results/finish/alignment_qa_report.done`
- Execution targets: `alignment_qa_report`
- Downstream handoff: `bam_stats`

## Guardrails
- Treat `results/finish/alignment_qa_report.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/alignment_qa_report.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `bam_stats` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/alignment_qa_report.done` exists and `bam_stats` can proceed without re-running alignment qa report.
