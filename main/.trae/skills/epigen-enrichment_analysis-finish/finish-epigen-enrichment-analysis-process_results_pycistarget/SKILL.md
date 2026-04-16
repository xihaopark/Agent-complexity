---
name: finish-epigen-enrichment-analysis-process_results_pycistarget
description: Use this skill when orchestrating the retained "process_results_pycisTarget" step of the epigen enrichment_analysis finish finish workflow. It keeps the process results pycisTarget stage tied to upstream `prepare_databases` and the downstream handoff to `region_enrichment_analysis_GREAT`. It tracks completion via `results/finish/process_results_pycisTarget.done`.
metadata:
  workflow_id: epigen-enrichment_analysis-finish
  workflow_name: epigen enrichment_analysis finish
  step_id: process_results_pycisTarget
  step_name: process results pycisTarget
---

# Scope
Use this skill only for the `process_results_pycisTarget` step in `epigen-enrichment_analysis-finish`.

## Orchestration
- Upstream requirements: `prepare_databases`
- Step file: `finish/epigen-enrichment_analysis-finish/steps/process_results_pycisTarget.smk`
- Config file: `finish/epigen-enrichment_analysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/process_results_pycisTarget.done`
- Representative outputs: `results/finish/process_results_pycisTarget.done`
- Execution targets: `process_results_pycisTarget`
- Downstream handoff: `region_enrichment_analysis_GREAT`

## Guardrails
- Treat `results/finish/process_results_pycisTarget.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/process_results_pycisTarget.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `region_enrichment_analysis_GREAT` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/process_results_pycisTarget.done` exists and `region_enrichment_analysis_GREAT` can proceed without re-running process results pycisTarget.
