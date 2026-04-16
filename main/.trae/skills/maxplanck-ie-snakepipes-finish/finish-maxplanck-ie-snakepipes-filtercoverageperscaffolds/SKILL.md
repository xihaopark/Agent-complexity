---
name: finish-maxplanck-ie-snakepipes-filtercoverageperscaffolds
description: Use this skill when orchestrating the retained "filterCoveragePerScaffolds" step of the maxplanck ie snakepipes finish finish workflow. It keeps the filterCoveragePerScaffolds stage tied to upstream `filterFragments` and the downstream handoff to `callOpenChromatin`. It tracks completion via `results/finish/filterCoveragePerScaffolds.done`.
metadata:
  workflow_id: maxplanck-ie-snakepipes-finish
  workflow_name: maxplanck ie snakepipes finish
  step_id: filterCoveragePerScaffolds
  step_name: filterCoveragePerScaffolds
---

# Scope
Use this skill only for the `filterCoveragePerScaffolds` step in `maxplanck-ie-snakepipes-finish`.

## Orchestration
- Upstream requirements: `filterFragments`
- Step file: `finish/maxplanck-ie-snakepipes-finish/steps/filterCoveragePerScaffolds.smk`
- Config file: `finish/maxplanck-ie-snakepipes-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/filterCoveragePerScaffolds.done`
- Representative outputs: `results/finish/filterCoveragePerScaffolds.done`
- Execution targets: `filterCoveragePerScaffolds`
- Downstream handoff: `callOpenChromatin`

## Guardrails
- Treat `results/finish/filterCoveragePerScaffolds.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/filterCoveragePerScaffolds.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `callOpenChromatin` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/filterCoveragePerScaffolds.done` exists and `callOpenChromatin` can proceed without re-running filterCoveragePerScaffolds.
