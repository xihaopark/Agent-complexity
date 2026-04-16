---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-plot_bootstrap
description: Use this skill when orchestrating the retained "plot_bootstrap" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the plot bootstrap stage tied to upstream `ihw_fdr_control` and the downstream handoff to `prepare_pca`. It tracks completion via `results/finish/plot_bootstrap.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: plot_bootstrap
  step_name: plot bootstrap
---

# Scope
Use this skill only for the `plot_bootstrap` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `ihw_fdr_control`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/plot_bootstrap.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plot_bootstrap.done`
- Representative outputs: `results/finish/plot_bootstrap.done`
- Execution targets: `plot_bootstrap`
- Downstream handoff: `prepare_pca`

## Guardrails
- Treat `results/finish/plot_bootstrap.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plot_bootstrap.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `prepare_pca` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plot_bootstrap.done` exists and `prepare_pca` can proceed without re-running plot bootstrap.
