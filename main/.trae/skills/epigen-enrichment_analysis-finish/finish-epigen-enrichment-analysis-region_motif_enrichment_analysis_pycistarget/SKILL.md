---
name: finish-epigen-enrichment-analysis-region_motif_enrichment_analysis_pycistarget
description: Use this skill when orchestrating the retained "region_motif_enrichment_analysis_pycisTarget" step of the epigen enrichment_analysis finish finish workflow. It keeps the region motif enrichment analysis pycisTarget stage tied to upstream `region_gene_association_GREAT` and the downstream handoff to `visualize`. It tracks completion via `results/finish/region_motif_enrichment_analysis_pycisTarget.done`.
metadata:
  workflow_id: epigen-enrichment_analysis-finish
  workflow_name: epigen enrichment_analysis finish
  step_id: region_motif_enrichment_analysis_pycisTarget
  step_name: region motif enrichment analysis pycisTarget
---

# Scope
Use this skill only for the `region_motif_enrichment_analysis_pycisTarget` step in `epigen-enrichment_analysis-finish`.

## Orchestration
- Upstream requirements: `region_gene_association_GREAT`
- Step file: `finish/epigen-enrichment_analysis-finish/steps/region_motif_enrichment_analysis_pycisTarget.smk`
- Config file: `finish/epigen-enrichment_analysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/region_motif_enrichment_analysis_pycisTarget.done`
- Representative outputs: `results/finish/region_motif_enrichment_analysis_pycisTarget.done`
- Execution targets: `region_motif_enrichment_analysis_pycisTarget`
- Downstream handoff: `visualize`

## Guardrails
- Treat `results/finish/region_motif_enrichment_analysis_pycisTarget.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/region_motif_enrichment_analysis_pycisTarget.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `visualize` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/region_motif_enrichment_analysis_pycisTarget.done` exists and `visualize` can proceed without re-running region motif enrichment analysis pycisTarget.
