---
name: finish-snakemake-workflows-rna-longseq-de-isoform-flair_diffexp
description: Use this skill when orchestrating the retained "flair_diffexp" step of the snakemake workflows rna longseq de isoform finish finish workflow. It keeps the flair diffexp stage tied to upstream `flair_quantify` and the downstream handoff to `flair_plot_isoforms`. It tracks completion via `results/finish/flair_diffexp.done`.
metadata:
  workflow_id: rna-longseq-de-isoform-finish
  workflow_name: snakemake workflows rna longseq de isoform finish
  step_id: flair_diffexp
  step_name: flair diffexp
---

# Scope
Use this skill only for the `flair_diffexp` step in `rna-longseq-de-isoform-finish`.

## Orchestration
- Upstream requirements: `flair_quantify`
- Step file: `finish/rna-longseq-de-isoform-finish/steps/flair_diffexp.smk`
- Config file: `finish/rna-longseq-de-isoform-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/flair_diffexp.done`
- Representative outputs: `results/finish/flair_diffexp.done`
- Execution targets: `flair_diffexp`
- Downstream handoff: `flair_plot_isoforms`

## Guardrails
- Treat `results/finish/flair_diffexp.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/flair_diffexp.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `flair_plot_isoforms` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/flair_diffexp.done` exists and `flair_plot_isoforms` can proceed without re-running flair diffexp.
