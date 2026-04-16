---
name: finish-maxplanck-ie-snakepipes-multibamsummary
description: Use this skill when orchestrating the retained "multiBamSummary" step of the maxplanck ie snakepipes finish finish workflow. It keeps the multiBamSummary stage tied to upstream `plotCoverage` and the downstream handoff to `plotCorrelation_pearson`. It tracks completion via `results/finish/multiBamSummary.done`.
metadata:
  workflow_id: maxplanck-ie-snakepipes-finish
  workflow_name: maxplanck ie snakepipes finish
  step_id: multiBamSummary
  step_name: multiBamSummary
---

# Scope
Use this skill only for the `multiBamSummary` step in `maxplanck-ie-snakepipes-finish`.

## Orchestration
- Upstream requirements: `plotCoverage`
- Step file: `finish/maxplanck-ie-snakepipes-finish/steps/multiBamSummary.smk`
- Config file: `finish/maxplanck-ie-snakepipes-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/multiBamSummary.done`
- Representative outputs: `results/finish/multiBamSummary.done`
- Execution targets: `multiBamSummary`
- Downstream handoff: `plotCorrelation_pearson`

## Guardrails
- Treat `results/finish/multiBamSummary.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/multiBamSummary.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plotCorrelation_pearson` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/multiBamSummary.done` exists and `plotCorrelation_pearson` can proceed without re-running multiBamSummary.
