---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-plot_scatter
description: Use this skill when orchestrating the retained "plot_scatter" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the plot scatter stage tied to upstream `plot_group_density` and the downstream handoff to `plot_fragment_length_dist`. It tracks completion via `results/finish/plot_scatter.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: plot_scatter
  step_name: plot scatter
---

# Scope
Use this skill only for the `plot_scatter` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `plot_group_density`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/plot_scatter.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plot_scatter.done`
- Representative outputs: `results/finish/plot_scatter.done`
- Execution targets: `plot_scatter`
- Downstream handoff: `plot_fragment_length_dist`

## Guardrails
- Treat `results/finish/plot_scatter.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plot_scatter.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plot_fragment_length_dist` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plot_scatter.done` exists and `plot_fragment_length_dist` can proceed without re-running plot scatter.
