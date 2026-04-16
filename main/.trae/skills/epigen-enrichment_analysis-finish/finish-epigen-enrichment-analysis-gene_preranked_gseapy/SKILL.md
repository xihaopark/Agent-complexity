---
name: finish-epigen-enrichment-analysis-gene_preranked_gseapy
description: Use this skill when orchestrating the retained "gene_preranked_GSEApy" step of the epigen enrichment_analysis finish finish workflow. It keeps the gene preranked GSEApy stage tied to upstream `gene_motif_enrichment_analysis_RcisTarget` and the downstream handoff to `plot_enrichment_result`. It tracks completion via `results/finish/gene_preranked_GSEApy.done`.
metadata:
  workflow_id: epigen-enrichment_analysis-finish
  workflow_name: epigen enrichment_analysis finish
  step_id: gene_preranked_GSEApy
  step_name: gene preranked GSEApy
---

# Scope
Use this skill only for the `gene_preranked_GSEApy` step in `epigen-enrichment_analysis-finish`.

## Orchestration
- Upstream requirements: `gene_motif_enrichment_analysis_RcisTarget`
- Step file: `finish/epigen-enrichment_analysis-finish/steps/gene_preranked_GSEApy.smk`
- Config file: `finish/epigen-enrichment_analysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/gene_preranked_GSEApy.done`
- Representative outputs: `results/finish/gene_preranked_GSEApy.done`
- Execution targets: `gene_preranked_GSEApy`
- Downstream handoff: `plot_enrichment_result`

## Guardrails
- Treat `results/finish/gene_preranked_GSEApy.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/gene_preranked_GSEApy.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plot_enrichment_result` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/gene_preranked_GSEApy.done` exists and `plot_enrichment_result` can proceed without re-running gene preranked GSEApy.
