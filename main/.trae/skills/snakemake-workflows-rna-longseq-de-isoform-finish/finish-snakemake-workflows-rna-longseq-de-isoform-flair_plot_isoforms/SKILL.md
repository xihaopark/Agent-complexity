---
name: finish-snakemake-workflows-rna-longseq-de-isoform-flair_plot_isoforms
description: Use this skill when orchestrating the retained "flair_plot_isoforms" step of the snakemake workflows rna longseq de isoform finish finish workflow. It keeps the flair plot isoforms stage tied to upstream `flair_diffexp` and the downstream handoff to `iso_analysis_report`. It tracks completion via `results/finish/flair_plot_isoforms.done`.
metadata:
  workflow_id: rna-longseq-de-isoform-finish
  workflow_name: snakemake workflows rna longseq de isoform finish
  step_id: flair_plot_isoforms
  step_name: flair plot isoforms
---

# Scope
Use this skill only for the `flair_plot_isoforms` step in `rna-longseq-de-isoform-finish`.

## Orchestration
- Upstream requirements: `flair_diffexp`
- Step file: `finish/rna-longseq-de-isoform-finish/steps/flair_plot_isoforms.smk`
- Config file: `finish/rna-longseq-de-isoform-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/flair_plot_isoforms.done`
- Representative outputs: `results/finish/flair_plot_isoforms.done`
- Execution targets: `flair_plot_isoforms`
- Downstream handoff: `iso_analysis_report`

## Guardrails
- Treat `results/finish/flair_plot_isoforms.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/flair_plot_isoforms.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `iso_analysis_report` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/flair_plot_isoforms.done` exists and `iso_analysis_report` can proceed without re-running flair plot isoforms.
