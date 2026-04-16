---
name: finish-epigen-enrichment-analysis-config_export
description: Use this skill when orchestrating the retained "config_export" step of the epigen enrichment_analysis finish finish workflow. It keeps the config export stage tied to upstream `annot_export` and the downstream handoff to `env_export`. It tracks completion via `results/finish/config_export.done`.
metadata:
  workflow_id: epigen-enrichment_analysis-finish
  workflow_name: epigen enrichment_analysis finish
  step_id: config_export
  step_name: config export
---

# Scope
Use this skill only for the `config_export` step in `epigen-enrichment_analysis-finish`.

## Orchestration
- Upstream requirements: `annot_export`
- Step file: `finish/epigen-enrichment_analysis-finish/steps/config_export.smk`
- Config file: `finish/epigen-enrichment_analysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/config_export.done`
- Representative outputs: `results/finish/config_export.done`
- Execution targets: `config_export`
- Downstream handoff: `env_export`

## Guardrails
- Treat `results/finish/config_export.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/config_export.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `env_export` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/config_export.done` exists and `env_export` can proceed without re-running config export.
