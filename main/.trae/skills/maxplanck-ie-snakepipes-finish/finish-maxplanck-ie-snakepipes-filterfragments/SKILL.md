---
name: finish-maxplanck-ie-snakepipes-filterfragments
description: Use this skill when orchestrating the retained "filterFragments" step of the maxplanck ie snakepipes finish finish workflow. It keeps the filterFragments stage tied to upstream `multiQC` and the downstream handoff to `filterCoveragePerScaffolds`. It tracks completion via `results/finish/filterFragments.done`.
metadata:
  workflow_id: maxplanck-ie-snakepipes-finish
  workflow_name: maxplanck ie snakepipes finish
  step_id: filterFragments
  step_name: filterFragments
---

# Scope
Use this skill only for the `filterFragments` step in `maxplanck-ie-snakepipes-finish`.

## Orchestration
- Upstream requirements: `multiQC`
- Step file: `finish/maxplanck-ie-snakepipes-finish/steps/filterFragments.smk`
- Config file: `finish/maxplanck-ie-snakepipes-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/filterFragments.done`
- Representative outputs: `results/finish/filterFragments.done`
- Execution targets: `filterFragments`
- Downstream handoff: `filterCoveragePerScaffolds`

## Guardrails
- Treat `results/finish/filterFragments.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/filterFragments.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `filterCoveragePerScaffolds` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/filterFragments.done` exists and `filterCoveragePerScaffolds` can proceed without re-running filterFragments.
