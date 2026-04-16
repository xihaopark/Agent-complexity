---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-plot_pathway_scatter
description: Use this skill when orchestrating the retained "plot_pathway_scatter" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the plot pathway scatter stage tied to upstream `plot_enrichment_scatter` and the downstream handoff to `spia_datavzrd`. It tracks completion via `results/finish/plot_pathway_scatter.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: plot_pathway_scatter
  step_name: plot pathway scatter
---

# Scope
Use this skill only for the `plot_pathway_scatter` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `plot_enrichment_scatter`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/plot_pathway_scatter.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plot_pathway_scatter.done`
- Representative outputs: `results/finish/plot_pathway_scatter.done`
- Execution targets: `plot_pathway_scatter`
- Downstream handoff: `spia_datavzrd`

## Guardrails
- Treat `results/finish/plot_pathway_scatter.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plot_pathway_scatter.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `spia_datavzrd` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plot_pathway_scatter.done` exists and `spia_datavzrd` can proceed without re-running plot pathway scatter.
