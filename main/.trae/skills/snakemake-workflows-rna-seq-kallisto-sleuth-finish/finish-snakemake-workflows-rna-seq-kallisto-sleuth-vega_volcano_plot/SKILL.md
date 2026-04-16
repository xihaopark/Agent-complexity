---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-vega_volcano_plot
description: Use this skill when orchestrating the retained "vega_volcano_plot" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the vega volcano plot stage tied to upstream `plot_vars` and the downstream handoff to `init_isoform_switch`. It tracks completion via `results/finish/vega_volcano_plot.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: vega_volcano_plot
  step_name: vega volcano plot
---

# Scope
Use this skill only for the `vega_volcano_plot` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `plot_vars`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/vega_volcano_plot.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/vega_volcano_plot.done`
- Representative outputs: `results/finish/vega_volcano_plot.done`
- Execution targets: `vega_volcano_plot`
- Downstream handoff: `init_isoform_switch`

## Guardrails
- Treat `results/finish/vega_volcano_plot.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/vega_volcano_plot.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `init_isoform_switch` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/vega_volcano_plot.done` exists and `init_isoform_switch` can proceed without re-running vega volcano plot.
