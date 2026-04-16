---
name: finish-epigen-enrichment-analysis-aggregate
description: Use this skill when orchestrating the retained "aggregate" step of the epigen enrichment_analysis finish finish workflow. It keeps the aggregate stage and the downstream handoff to `annot_export`. It tracks completion via `results/finish/aggregate.done`.
metadata:
  workflow_id: epigen-enrichment_analysis-finish
  workflow_name: epigen enrichment_analysis finish
  step_id: aggregate
  step_name: aggregate
---

# Scope
Use this skill only for the `aggregate` step in `epigen-enrichment_analysis-finish`.

## Orchestration
- Upstream requirements: none
- Step file: `finish/epigen-enrichment_analysis-finish/steps/aggregate.smk`
- Config file: `finish/epigen-enrichment_analysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/aggregate.done`
- Representative outputs: `results/finish/aggregate.done`
- Execution targets: `aggregate`
- Downstream handoff: `annot_export`

## Guardrails
- Treat `results/finish/aggregate.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/aggregate.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `annot_export` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/aggregate.done` exists and `annot_export` can proceed without re-running aggregate.
