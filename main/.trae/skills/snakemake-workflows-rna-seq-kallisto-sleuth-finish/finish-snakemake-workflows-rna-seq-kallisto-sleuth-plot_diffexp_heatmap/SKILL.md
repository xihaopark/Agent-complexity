---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-plot_diffexp_heatmap
description: Use this skill when orchestrating the retained "plot_diffexp_heatmap" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the plot diffexp heatmap stage tied to upstream `tpm_matrix` and the downstream handoff to `plot_group_density`. It tracks completion via `results/finish/plot_diffexp_heatmap.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: plot_diffexp_heatmap
  step_name: plot diffexp heatmap
---

# Scope
Use this skill only for the `plot_diffexp_heatmap` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `tpm_matrix`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/plot_diffexp_heatmap.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plot_diffexp_heatmap.done`
- Representative outputs: `results/finish/plot_diffexp_heatmap.done`
- Execution targets: `plot_diffexp_heatmap`
- Downstream handoff: `plot_group_density`

## Guardrails
- Treat `results/finish/plot_diffexp_heatmap.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plot_diffexp_heatmap.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plot_group_density` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plot_diffexp_heatmap.done` exists and `plot_group_density` can proceed without re-running plot diffexp heatmap.
