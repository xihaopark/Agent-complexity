---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-plot_group_density
description: Use this skill when orchestrating the retained "plot_group_density" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the plot group density stage tied to upstream `plot_diffexp_heatmap` and the downstream handoff to `plot_scatter`. It tracks completion via `results/finish/plot_group_density.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: plot_group_density
  step_name: plot group density
---

# Scope
Use this skill only for the `plot_group_density` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `plot_diffexp_heatmap`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/plot_group_density.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plot_group_density.done`
- Representative outputs: `results/finish/plot_group_density.done`
- Execution targets: `plot_group_density`
- Downstream handoff: `plot_scatter`

## Guardrails
- Treat `results/finish/plot_group_density.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plot_group_density.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plot_scatter` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plot_group_density.done` exists and `plot_scatter` can proceed without re-running plot group density.
