---
name: finish-epigen-enrichment-analysis-plot_enrichment_result
description: Use this skill when orchestrating the retained "plot_enrichment_result" step of the epigen enrichment_analysis finish finish workflow. It keeps the plot enrichment result stage tied to upstream `gene_preranked_GSEApy` and the downstream handoff to `prepare_databases`. It tracks completion via `results/finish/plot_enrichment_result.done`.
metadata:
  workflow_id: epigen-enrichment_analysis-finish
  workflow_name: epigen enrichment_analysis finish
  step_id: plot_enrichment_result
  step_name: plot enrichment result
---

# Scope
Use this skill only for the `plot_enrichment_result` step in `epigen-enrichment_analysis-finish`.

## Orchestration
- Upstream requirements: `gene_preranked_GSEApy`
- Step file: `finish/epigen-enrichment_analysis-finish/steps/plot_enrichment_result.smk`
- Config file: `finish/epigen-enrichment_analysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plot_enrichment_result.done`
- Representative outputs: `results/finish/plot_enrichment_result.done`
- Execution targets: `plot_enrichment_result`
- Downstream handoff: `prepare_databases`

## Guardrails
- Treat `results/finish/plot_enrichment_result.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plot_enrichment_result.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `prepare_databases` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plot_enrichment_result.done` exists and `prepare_databases` can proceed without re-running plot enrichment result.
