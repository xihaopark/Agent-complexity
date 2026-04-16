---
name: finish-epigen-enrichment-analysis-region_enrichment_analysis_lola
description: Use this skill when orchestrating the retained "region_enrichment_analysis_LOLA" step of the epigen enrichment_analysis finish finish workflow. It keeps the region enrichment analysis LOLA stage tied to upstream `region_enrichment_analysis_GREAT` and the downstream handoff to `region_gene_association_GREAT`. It tracks completion via `results/finish/region_enrichment_analysis_LOLA.done`.
metadata:
  workflow_id: epigen-enrichment_analysis-finish
  workflow_name: epigen enrichment_analysis finish
  step_id: region_enrichment_analysis_LOLA
  step_name: region enrichment analysis LOLA
---

# Scope
Use this skill only for the `region_enrichment_analysis_LOLA` step in `epigen-enrichment_analysis-finish`.

## Orchestration
- Upstream requirements: `region_enrichment_analysis_GREAT`
- Step file: `finish/epigen-enrichment_analysis-finish/steps/region_enrichment_analysis_LOLA.smk`
- Config file: `finish/epigen-enrichment_analysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/region_enrichment_analysis_LOLA.done`
- Representative outputs: `results/finish/region_enrichment_analysis_LOLA.done`
- Execution targets: `region_enrichment_analysis_LOLA`
- Downstream handoff: `region_gene_association_GREAT`

## Guardrails
- Treat `results/finish/region_enrichment_analysis_LOLA.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/region_enrichment_analysis_LOLA.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `region_gene_association_GREAT` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/region_enrichment_analysis_LOLA.done` exists and `region_gene_association_GREAT` can proceed without re-running region enrichment analysis LOLA.
