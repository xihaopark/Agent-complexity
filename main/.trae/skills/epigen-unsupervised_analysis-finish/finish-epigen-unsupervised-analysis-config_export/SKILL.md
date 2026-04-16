---
name: finish-epigen-unsupervised-analysis-config_export
description: Use this skill when orchestrating the retained "config_export" step of the epigen unsupervised_analysis finish finish workflow. It keeps the config export stage tied to upstream `clustree_analysis_metadata` and the downstream handoff to `densmap_embed`. It tracks completion via `results/finish/config_export.done`.
metadata:
  workflow_id: epigen-unsupervised_analysis-finish
  workflow_name: epigen unsupervised_analysis finish
  step_id: config_export
  step_name: config export
---

# Scope
Use this skill only for the `config_export` step in `epigen-unsupervised_analysis-finish`.

## Orchestration
- Upstream requirements: `clustree_analysis_metadata`
- Step file: `finish/epigen-unsupervised_analysis-finish/steps/config_export.smk`
- Config file: `finish/epigen-unsupervised_analysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/config_export.done`
- Representative outputs: `results/finish/config_export.done`
- Execution targets: `config_export`
- Downstream handoff: `densmap_embed`

## Guardrails
- Treat `results/finish/config_export.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/config_export.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `densmap_embed` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/config_export.done` exists and `densmap_embed` can proceed without re-running config export.
