---
name: finish-snakemake-workflows-rna-longseq-de-isoform-iso_analysis_report
description: Use this skill when orchestrating the retained "iso_analysis_report" step of the snakemake workflows rna longseq de isoform finish finish workflow. It keeps the iso analysis report stage tied to upstream `flair_plot_isoforms` and the downstream handoff to `get_indexed_protein_db`. It tracks completion via `results/finish/iso_analysis_report.done`.
metadata:
  workflow_id: rna-longseq-de-isoform-finish
  workflow_name: snakemake workflows rna longseq de isoform finish
  step_id: iso_analysis_report
  step_name: iso analysis report
---

# Scope
Use this skill only for the `iso_analysis_report` step in `rna-longseq-de-isoform-finish`.

## Orchestration
- Upstream requirements: `flair_plot_isoforms`
- Step file: `finish/rna-longseq-de-isoform-finish/steps/iso_analysis_report.smk`
- Config file: `finish/rna-longseq-de-isoform-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/iso_analysis_report.done`
- Representative outputs: `results/finish/iso_analysis_report.done`
- Execution targets: `iso_analysis_report`
- Downstream handoff: `get_indexed_protein_db`

## Guardrails
- Treat `results/finish/iso_analysis_report.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/iso_analysis_report.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `get_indexed_protein_db` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/iso_analysis_report.done` exists and `get_indexed_protein_db` can proceed without re-running iso analysis report.
