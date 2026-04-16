---
name: finish-epigen-unsupervised-analysis-clustree_analysis
description: Use this skill when orchestrating the retained "clustree_analysis" step of the epigen unsupervised_analysis finish finish workflow. It keeps the clustree analysis stage tied to upstream `annot_export` and the downstream handoff to `clustree_analysis_metadata`. It tracks completion via `results/finish/clustree_analysis.done`.
metadata:
  workflow_id: epigen-unsupervised_analysis-finish
  workflow_name: epigen unsupervised_analysis finish
  step_id: clustree_analysis
  step_name: clustree analysis
---

# Scope
Use this skill only for the `clustree_analysis` step in `epigen-unsupervised_analysis-finish`.

## Orchestration
- Upstream requirements: `annot_export`
- Step file: `finish/epigen-unsupervised_analysis-finish/steps/clustree_analysis.smk`
- Config file: `finish/epigen-unsupervised_analysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/clustree_analysis.done`
- Representative outputs: `results/finish/clustree_analysis.done`
- Execution targets: `clustree_analysis`
- Downstream handoff: `clustree_analysis_metadata`

## Guardrails
- Treat `results/finish/clustree_analysis.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/clustree_analysis.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `clustree_analysis_metadata` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/clustree_analysis.done` exists and `clustree_analysis_metadata` can proceed without re-running clustree analysis.
