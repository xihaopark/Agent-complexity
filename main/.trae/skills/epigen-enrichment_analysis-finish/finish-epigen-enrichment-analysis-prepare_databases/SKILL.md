---
name: finish-epigen-enrichment-analysis-prepare_databases
description: Use this skill when orchestrating the retained "prepare_databases" step of the epigen enrichment_analysis finish finish workflow. It keeps the prepare databases stage tied to upstream `plot_enrichment_result` and the downstream handoff to `process_results_pycisTarget`. It tracks completion via `results/finish/prepare_databases.done`.
metadata:
  workflow_id: epigen-enrichment_analysis-finish
  workflow_name: epigen enrichment_analysis finish
  step_id: prepare_databases
  step_name: prepare databases
---

# Scope
Use this skill only for the `prepare_databases` step in `epigen-enrichment_analysis-finish`.

## Orchestration
- Upstream requirements: `plot_enrichment_result`
- Step file: `finish/epigen-enrichment_analysis-finish/steps/prepare_databases.smk`
- Config file: `finish/epigen-enrichment_analysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/prepare_databases.done`
- Representative outputs: `results/finish/prepare_databases.done`
- Execution targets: `prepare_databases`
- Downstream handoff: `process_results_pycisTarget`

## Guardrails
- Treat `results/finish/prepare_databases.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/prepare_databases.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `process_results_pycisTarget` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/prepare_databases.done` exists and `process_results_pycisTarget` can proceed without re-running prepare databases.
