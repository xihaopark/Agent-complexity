---
name: finish-maxplanck-ie-snakepipes-plotcorrelation_spearman
description: Use this skill when orchestrating the retained "plotCorrelation_spearman" step of the maxplanck ie snakepipes finish finish workflow. It keeps the plotCorrelation spearman stage tied to upstream `plotCorrelation_pearson` and the downstream handoff to `plotPCA`. It tracks completion via `results/finish/plotCorrelation_spearman.done`.
metadata:
  workflow_id: maxplanck-ie-snakepipes-finish
  workflow_name: maxplanck ie snakepipes finish
  step_id: plotCorrelation_spearman
  step_name: plotCorrelation spearman
---

# Scope
Use this skill only for the `plotCorrelation_spearman` step in `maxplanck-ie-snakepipes-finish`.

## Orchestration
- Upstream requirements: `plotCorrelation_pearson`
- Step file: `finish/maxplanck-ie-snakepipes-finish/steps/plotCorrelation_spearman.smk`
- Config file: `finish/maxplanck-ie-snakepipes-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plotCorrelation_spearman.done`
- Representative outputs: `results/finish/plotCorrelation_spearman.done`
- Execution targets: `plotCorrelation_spearman`
- Downstream handoff: `plotPCA`

## Guardrails
- Treat `results/finish/plotCorrelation_spearman.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plotCorrelation_spearman.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plotPCA` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plotCorrelation_spearman.done` exists and `plotPCA` can proceed without re-running plotCorrelation spearman.
