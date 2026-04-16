---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-plot_vars
description: Use this skill when orchestrating the retained "plot_vars" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the plot vars stage tied to upstream `plot_fragment_length_dist` and the downstream handoff to `vega_volcano_plot`. It tracks completion via `results/finish/plot_vars.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: plot_vars
  step_name: plot vars
---

# Scope
Use this skill only for the `plot_vars` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `plot_fragment_length_dist`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/plot_vars.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plot_vars.done`
- Representative outputs: `results/finish/plot_vars.done`
- Execution targets: `plot_vars`
- Downstream handoff: `vega_volcano_plot`

## Guardrails
- Treat `results/finish/plot_vars.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plot_vars.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `vega_volcano_plot` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plot_vars.done` exists and `vega_volcano_plot` can proceed without re-running plot vars.
