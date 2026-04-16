---
name: finish-maxplanck-ie-snakepipes-plotpca
description: Use this skill when orchestrating the retained "plotPCA" step of the maxplanck ie snakepipes finish finish workflow. It keeps the plotPCA stage tied to upstream `plotCorrelation_spearman` and the downstream handoff to `estimate_read_filtering`. It tracks completion via `results/finish/plotPCA.done`.
metadata:
  workflow_id: maxplanck-ie-snakepipes-finish
  workflow_name: maxplanck ie snakepipes finish
  step_id: plotPCA
  step_name: plotPCA
---

# Scope
Use this skill only for the `plotPCA` step in `maxplanck-ie-snakepipes-finish`.

## Orchestration
- Upstream requirements: `plotCorrelation_spearman`
- Step file: `finish/maxplanck-ie-snakepipes-finish/steps/plotPCA.smk`
- Config file: `finish/maxplanck-ie-snakepipes-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plotPCA.done`
- Representative outputs: `results/finish/plotPCA.done`
- Execution targets: `plotPCA`
- Downstream handoff: `estimate_read_filtering`

## Guardrails
- Treat `results/finish/plotPCA.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plotPCA.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `estimate_read_filtering` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plotPCA.done` exists and `estimate_read_filtering` can proceed without re-running plotPCA.
