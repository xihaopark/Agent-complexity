---
name: finish-epigen-dea-limma-aggregate
description: Use this skill when orchestrating the retained "aggregate" step of the epigen dea_limma finish finish workflow. It keeps the aggregate stage tied to upstream `one_vs_all_contrasts` and the downstream handoff to `ova_stats_plot`. It tracks completion via `results/finish/aggregate.done`.
metadata:
  workflow_id: epigen-dea_limma-finish
  workflow_name: epigen dea_limma finish
  step_id: aggregate
  step_name: aggregate
---

# Scope
Use this skill only for the `aggregate` step in `epigen-dea_limma-finish`.

## Orchestration
- Upstream requirements: `one_vs_all_contrasts`
- Step file: `finish/epigen-dea_limma-finish/steps/aggregate.smk`
- Config file: `finish/epigen-dea_limma-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/aggregate.done`
- Representative outputs: `results/finish/aggregate.done`
- Execution targets: `aggregate`
- Downstream handoff: `ova_stats_plot`

## Guardrails
- Treat `results/finish/aggregate.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/aggregate.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ova_stats_plot` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/aggregate.done` exists and `ova_stats_plot` can proceed without re-running aggregate.
