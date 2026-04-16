---
name: finish-epigen-unsupervised-analysis-clustree_analysis_metadata
description: Use this skill when orchestrating the retained "clustree_analysis_metadata" step of the epigen unsupervised_analysis finish finish workflow. It keeps the clustree analysis metadata stage tied to upstream `clustree_analysis` and the downstream handoff to `config_export`. It tracks completion via `results/finish/clustree_analysis_metadata.done`.
metadata:
  workflow_id: epigen-unsupervised_analysis-finish
  workflow_name: epigen unsupervised_analysis finish
  step_id: clustree_analysis_metadata
  step_name: clustree analysis metadata
---

# Scope
Use this skill only for the `clustree_analysis_metadata` step in `epigen-unsupervised_analysis-finish`.

## Orchestration
- Upstream requirements: `clustree_analysis`
- Step file: `finish/epigen-unsupervised_analysis-finish/steps/clustree_analysis_metadata.smk`
- Config file: `finish/epigen-unsupervised_analysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/clustree_analysis_metadata.done`
- Representative outputs: `results/finish/clustree_analysis_metadata.done`
- Execution targets: `clustree_analysis_metadata`
- Downstream handoff: `config_export`

## Guardrails
- Treat `results/finish/clustree_analysis_metadata.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/clustree_analysis_metadata.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `config_export` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/clustree_analysis_metadata.done` exists and `config_export` can proceed without re-running clustree analysis metadata.
