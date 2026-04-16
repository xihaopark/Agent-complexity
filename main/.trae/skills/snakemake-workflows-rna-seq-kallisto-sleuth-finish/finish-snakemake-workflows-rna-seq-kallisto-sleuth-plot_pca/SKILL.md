---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-plot_pca
description: Use this skill when orchestrating the retained "plot_pca" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the plot pca stage tied to upstream `prepare_pca` and the downstream handoff to `plot_diffexp_pval_hist`. It tracks completion via `results/finish/plot_pca.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: plot_pca
  step_name: plot pca
---

# Scope
Use this skill only for the `plot_pca` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `prepare_pca`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/plot_pca.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plot_pca.done`
- Representative outputs: `results/finish/plot_pca.done`
- Execution targets: `plot_pca`
- Downstream handoff: `plot_diffexp_pval_hist`

## Guardrails
- Treat `results/finish/plot_pca.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plot_pca.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plot_diffexp_pval_hist` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plot_pca.done` exists and `plot_diffexp_pval_hist` can proceed without re-running plot pca.
