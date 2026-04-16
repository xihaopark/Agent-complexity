---
name: finish-snakemake-workflows-rna-longseq-de-isoform-total_sample_qa_plot
description: Use this skill when orchestrating the retained "total_sample_qa_plot" step of the snakemake workflows rna longseq de isoform finish finish workflow. It keeps the total sample qa plot stage tied to upstream `sample_qa_plot` and the downstream handoff to `alignment_qa`. It tracks completion via `results/finish/total_sample_qa_plot.done`.
metadata:
  workflow_id: rna-longseq-de-isoform-finish
  workflow_name: snakemake workflows rna longseq de isoform finish
  step_id: total_sample_qa_plot
  step_name: total sample qa plot
---

# Scope
Use this skill only for the `total_sample_qa_plot` step in `rna-longseq-de-isoform-finish`.

## Orchestration
- Upstream requirements: `sample_qa_plot`
- Step file: `finish/rna-longseq-de-isoform-finish/steps/total_sample_qa_plot.smk`
- Config file: `finish/rna-longseq-de-isoform-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/total_sample_qa_plot.done`
- Representative outputs: `results/finish/total_sample_qa_plot.done`
- Execution targets: `total_sample_qa_plot`
- Downstream handoff: `alignment_qa`

## Guardrails
- Treat `results/finish/total_sample_qa_plot.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/total_sample_qa_plot.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `alignment_qa` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/total_sample_qa_plot.done` exists and `alignment_qa` can proceed without re-running total sample qa plot.
