---
name: finish-epigen-enrichment-analysis-region_enrichment_analysis_great
description: Use this skill when orchestrating the retained "region_enrichment_analysis_GREAT" step of the epigen enrichment_analysis finish finish workflow. It keeps the region enrichment analysis GREAT stage tied to upstream `process_results_pycisTarget` and the downstream handoff to `region_enrichment_analysis_LOLA`. It tracks completion via `results/finish/region_enrichment_analysis_GREAT.done`.
metadata:
  workflow_id: epigen-enrichment_analysis-finish
  workflow_name: epigen enrichment_analysis finish
  step_id: region_enrichment_analysis_GREAT
  step_name: region enrichment analysis GREAT
---

# Scope
Use this skill only for the `region_enrichment_analysis_GREAT` step in `epigen-enrichment_analysis-finish`.

## Orchestration
- Upstream requirements: `process_results_pycisTarget`
- Step file: `finish/epigen-enrichment_analysis-finish/steps/region_enrichment_analysis_GREAT.smk`
- Config file: `finish/epigen-enrichment_analysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/region_enrichment_analysis_GREAT.done`
- Representative outputs: `results/finish/region_enrichment_analysis_GREAT.done`
- Execution targets: `region_enrichment_analysis_GREAT`
- Downstream handoff: `region_enrichment_analysis_LOLA`

## Guardrails
- Treat `results/finish/region_enrichment_analysis_GREAT.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/region_enrichment_analysis_GREAT.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `region_enrichment_analysis_LOLA` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/region_enrichment_analysis_GREAT.done` exists and `region_enrichment_analysis_LOLA` can proceed without re-running region enrichment analysis GREAT.
