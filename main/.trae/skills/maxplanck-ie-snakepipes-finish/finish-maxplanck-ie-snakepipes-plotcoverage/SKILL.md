---
name: finish-maxplanck-ie-snakepipes-plotcoverage
description: Use this skill when orchestrating the retained "plotCoverage" step of the maxplanck ie snakepipes finish finish workflow. It keeps the plotCoverage stage tied to upstream `bamCoverage_filtered` and the downstream handoff to `multiBamSummary`. It tracks completion via `results/finish/plotCoverage.done`.
metadata:
  workflow_id: maxplanck-ie-snakepipes-finish
  workflow_name: maxplanck ie snakepipes finish
  step_id: plotCoverage
  step_name: plotCoverage
---

# Scope
Use this skill only for the `plotCoverage` step in `maxplanck-ie-snakepipes-finish`.

## Orchestration
- Upstream requirements: `bamCoverage_filtered`
- Step file: `finish/maxplanck-ie-snakepipes-finish/steps/plotCoverage.smk`
- Config file: `finish/maxplanck-ie-snakepipes-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plotCoverage.done`
- Representative outputs: `results/finish/plotCoverage.done`
- Execution targets: `plotCoverage`
- Downstream handoff: `multiBamSummary`

## Guardrails
- Treat `results/finish/plotCoverage.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plotCoverage.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `multiBamSummary` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plotCoverage.done` exists and `multiBamSummary` can proceed without re-running plotCoverage.
