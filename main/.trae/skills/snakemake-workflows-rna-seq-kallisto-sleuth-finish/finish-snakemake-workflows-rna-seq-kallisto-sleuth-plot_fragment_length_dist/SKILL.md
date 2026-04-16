---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-plot_fragment_length_dist
description: Use this skill when orchestrating the retained "plot_fragment_length_dist" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the plot fragment length dist stage tied to upstream `plot_scatter` and the downstream handoff to `plot_vars`. It tracks completion via `results/finish/plot_fragment_length_dist.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: plot_fragment_length_dist
  step_name: plot fragment length dist
---

# Scope
Use this skill only for the `plot_fragment_length_dist` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `plot_scatter`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/plot_fragment_length_dist.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plot_fragment_length_dist.done`
- Representative outputs: `results/finish/plot_fragment_length_dist.done`
- Execution targets: `plot_fragment_length_dist`
- Downstream handoff: `plot_vars`

## Guardrails
- Treat `results/finish/plot_fragment_length_dist.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plot_fragment_length_dist.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plot_vars` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plot_fragment_length_dist.done` exists and `plot_vars` can proceed without re-running plot fragment length dist.
