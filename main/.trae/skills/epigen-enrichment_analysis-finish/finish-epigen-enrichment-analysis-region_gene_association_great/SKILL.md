---
name: finish-epigen-enrichment-analysis-region_gene_association_great
description: Use this skill when orchestrating the retained "region_gene_association_GREAT" step of the epigen enrichment_analysis finish finish workflow. It keeps the region gene association GREAT stage tied to upstream `region_enrichment_analysis_LOLA` and the downstream handoff to `region_motif_enrichment_analysis_pycisTarget`. It tracks completion via `results/finish/region_gene_association_GREAT.done`.
metadata:
  workflow_id: epigen-enrichment_analysis-finish
  workflow_name: epigen enrichment_analysis finish
  step_id: region_gene_association_GREAT
  step_name: region gene association GREAT
---

# Scope
Use this skill only for the `region_gene_association_GREAT` step in `epigen-enrichment_analysis-finish`.

## Orchestration
- Upstream requirements: `region_enrichment_analysis_LOLA`
- Step file: `finish/epigen-enrichment_analysis-finish/steps/region_gene_association_GREAT.smk`
- Config file: `finish/epigen-enrichment_analysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/region_gene_association_GREAT.done`
- Representative outputs: `results/finish/region_gene_association_GREAT.done`
- Execution targets: `region_gene_association_GREAT`
- Downstream handoff: `region_motif_enrichment_analysis_pycisTarget`

## Guardrails
- Treat `results/finish/region_gene_association_GREAT.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/region_gene_association_GREAT.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `region_motif_enrichment_analysis_pycisTarget` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/region_gene_association_GREAT.done` exists and `region_motif_enrichment_analysis_pycisTarget` can proceed without re-running region gene association GREAT.
