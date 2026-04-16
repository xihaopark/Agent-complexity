---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-plot_enrichment_scatter
description: Use this skill when orchestrating the retained "plot_enrichment_scatter" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the plot enrichment scatter stage tied to upstream `postprocess_tpm_matrix` and the downstream handoff to `plot_pathway_scatter`. It tracks completion via `results/finish/plot_enrichment_scatter.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: plot_enrichment_scatter
  step_name: plot enrichment scatter
---

# Scope
Use this skill only for the `plot_enrichment_scatter` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `postprocess_tpm_matrix`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/plot_enrichment_scatter.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plot_enrichment_scatter.done`
- Representative outputs: `results/finish/plot_enrichment_scatter.done`
- Execution targets: `plot_enrichment_scatter`
- Downstream handoff: `plot_pathway_scatter`

## Guardrails
- Treat `results/finish/plot_enrichment_scatter.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plot_enrichment_scatter.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plot_pathway_scatter` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plot_enrichment_scatter.done` exists and `plot_pathway_scatter` can proceed without re-running plot enrichment scatter.
