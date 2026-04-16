---
name: finish-snakemake-workflows-rna-longseq-de-isoform-alignment_qa
description: Use this skill when orchestrating the retained "alignment_qa" step of the snakemake workflows rna longseq de isoform finish finish workflow. It keeps the alignment qa stage tied to upstream `total_sample_qa_plot` and the downstream handoff to `alignment_qa_report`. It tracks completion via `results/finish/alignment_qa.done`.
metadata:
  workflow_id: rna-longseq-de-isoform-finish
  workflow_name: snakemake workflows rna longseq de isoform finish
  step_id: alignment_qa
  step_name: alignment qa
---

# Scope
Use this skill only for the `alignment_qa` step in `rna-longseq-de-isoform-finish`.

## Orchestration
- Upstream requirements: `total_sample_qa_plot`
- Step file: `finish/rna-longseq-de-isoform-finish/steps/alignment_qa.smk`
- Config file: `finish/rna-longseq-de-isoform-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/alignment_qa.done`
- Representative outputs: `results/finish/alignment_qa.done`
- Execution targets: `alignment_qa`
- Downstream handoff: `alignment_qa_report`

## Guardrails
- Treat `results/finish/alignment_qa.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/alignment_qa.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `alignment_qa_report` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/alignment_qa.done` exists and `alignment_qa_report` can proceed without re-running alignment qa.
