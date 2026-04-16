---
name: finish-snakemake-workflows-rna-longseq-de-isoform-sample_qa_plot
description: Use this skill when orchestrating the retained "sample_qa_plot" step of the snakemake workflows rna longseq de isoform finish finish workflow. It keeps the sample qa plot stage and the downstream handoff to `total_sample_qa_plot`. It tracks completion via `results/finish/sample_qa_plot.done`.
metadata:
  workflow_id: rna-longseq-de-isoform-finish
  workflow_name: snakemake workflows rna longseq de isoform finish
  step_id: sample_qa_plot
  step_name: sample qa plot
---

# Scope
Use this skill only for the `sample_qa_plot` step in `rna-longseq-de-isoform-finish`.

## Orchestration
- Upstream requirements: none
- Step file: `finish/rna-longseq-de-isoform-finish/steps/sample_qa_plot.smk`
- Config file: `finish/rna-longseq-de-isoform-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/sample_qa_plot.done`
- Representative outputs: `results/finish/sample_qa_plot.done`
- Execution targets: `sample_qa_plot`
- Downstream handoff: `total_sample_qa_plot`

## Guardrails
- Treat `results/finish/sample_qa_plot.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/sample_qa_plot.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `total_sample_qa_plot` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/sample_qa_plot.done` exists and `total_sample_qa_plot` can proceed without re-running sample qa plot.
