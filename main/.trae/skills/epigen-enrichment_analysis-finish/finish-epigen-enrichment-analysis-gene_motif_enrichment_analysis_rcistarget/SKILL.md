---
name: finish-epigen-enrichment-analysis-gene_motif_enrichment_analysis_rcistarget
description: Use this skill when orchestrating the retained "gene_motif_enrichment_analysis_RcisTarget" step of the epigen enrichment_analysis finish finish workflow. It keeps the gene motif enrichment analysis RcisTarget stage tied to upstream `gene_ORA_GSEApy` and the downstream handoff to `gene_preranked_GSEApy`. It tracks completion via `results/finish/gene_motif_enrichment_analysis_RcisTarget.done`.
metadata:
  workflow_id: epigen-enrichment_analysis-finish
  workflow_name: epigen enrichment_analysis finish
  step_id: gene_motif_enrichment_analysis_RcisTarget
  step_name: gene motif enrichment analysis RcisTarget
---

# Scope
Use this skill only for the `gene_motif_enrichment_analysis_RcisTarget` step in `epigen-enrichment_analysis-finish`.

## Orchestration
- Upstream requirements: `gene_ORA_GSEApy`
- Step file: `finish/epigen-enrichment_analysis-finish/steps/gene_motif_enrichment_analysis_RcisTarget.smk`
- Config file: `finish/epigen-enrichment_analysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/gene_motif_enrichment_analysis_RcisTarget.done`
- Representative outputs: `results/finish/gene_motif_enrichment_analysis_RcisTarget.done`
- Execution targets: `gene_motif_enrichment_analysis_RcisTarget`
- Downstream handoff: `gene_preranked_GSEApy`

## Guardrails
- Treat `results/finish/gene_motif_enrichment_analysis_RcisTarget.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/gene_motif_enrichment_analysis_RcisTarget.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `gene_preranked_GSEApy` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/gene_motif_enrichment_analysis_RcisTarget.done` exists and `gene_preranked_GSEApy` can proceed without re-running gene motif enrichment analysis RcisTarget.
