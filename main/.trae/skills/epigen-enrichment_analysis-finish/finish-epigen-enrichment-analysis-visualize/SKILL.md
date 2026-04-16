---
name: finish-epigen-enrichment-analysis-visualize
description: Use this skill when orchestrating the retained "visualize" step of the epigen enrichment_analysis finish finish workflow. It keeps the visualize stage tied to upstream `region_motif_enrichment_analysis_pycisTarget` and the downstream handoff to `all`. It tracks completion via `results/finish/visualize.done`.
metadata:
  workflow_id: epigen-enrichment_analysis-finish
  workflow_name: epigen enrichment_analysis finish
  step_id: visualize
  step_name: visualize
---

# Scope
Use this skill only for the `visualize` step in `epigen-enrichment_analysis-finish`.

## Orchestration
- Upstream requirements: `region_motif_enrichment_analysis_pycisTarget`
- Step file: `finish/epigen-enrichment_analysis-finish/steps/visualize.smk`
- Config file: `finish/epigen-enrichment_analysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/visualize.done`
- Representative outputs: `results/finish/visualize.done`
- Execution targets: `visualize`
- Downstream handoff: `all`

## Guardrails
- Treat `results/finish/visualize.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/visualize.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `all` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/visualize.done` exists and `all` can proceed without re-running visualize.
