---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-plot_diffexp_pval_hist
description: Use this skill when orchestrating the retained "plot_diffexp_pval_hist" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the plot diffexp pval hist stage tied to upstream `plot_pca` and the downstream handoff to `logcount_matrix`. It tracks completion via `results/finish/plot_diffexp_pval_hist.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: plot_diffexp_pval_hist
  step_name: plot diffexp pval hist
---

# Scope
Use this skill only for the `plot_diffexp_pval_hist` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `plot_pca`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/plot_diffexp_pval_hist.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plot_diffexp_pval_hist.done`
- Representative outputs: `results/finish/plot_diffexp_pval_hist.done`
- Execution targets: `plot_diffexp_pval_hist`
- Downstream handoff: `logcount_matrix`

## Guardrails
- Treat `results/finish/plot_diffexp_pval_hist.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plot_diffexp_pval_hist.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `logcount_matrix` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plot_diffexp_pval_hist.done` exists and `logcount_matrix` can proceed without re-running plot diffexp pval hist.
