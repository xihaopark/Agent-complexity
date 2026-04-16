---
name: finish-maxplanck-ie-snakepipes-plotcorrelation_pearson
description: Use this skill when orchestrating the retained "plotCorrelation_pearson" step of the maxplanck ie snakepipes finish finish workflow. It keeps the plotCorrelation pearson stage tied to upstream `multiBamSummary` and the downstream handoff to `plotCorrelation_spearman`. It tracks completion via `results/finish/plotCorrelation_pearson.done`.
metadata:
  workflow_id: maxplanck-ie-snakepipes-finish
  workflow_name: maxplanck ie snakepipes finish
  step_id: plotCorrelation_pearson
  step_name: plotCorrelation pearson
---

# Scope
Use this skill only for the `plotCorrelation_pearson` step in `maxplanck-ie-snakepipes-finish`.

## Orchestration
- Upstream requirements: `multiBamSummary`
- Step file: `finish/maxplanck-ie-snakepipes-finish/steps/plotCorrelation_pearson.smk`
- Config file: `finish/maxplanck-ie-snakepipes-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plotCorrelation_pearson.done`
- Representative outputs: `results/finish/plotCorrelation_pearson.done`
- Execution targets: `plotCorrelation_pearson`
- Downstream handoff: `plotCorrelation_spearman`

## Guardrails
- Treat `results/finish/plotCorrelation_pearson.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plotCorrelation_pearson.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plotCorrelation_spearman` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plotCorrelation_pearson.done` exists and `plotCorrelation_spearman` can proceed without re-running plotCorrelation pearson.
