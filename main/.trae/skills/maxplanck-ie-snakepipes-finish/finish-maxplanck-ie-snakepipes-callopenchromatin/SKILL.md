---
name: finish-maxplanck-ie-snakepipes-callopenchromatin
description: Use this skill when orchestrating the retained "callOpenChromatin" step of the maxplanck ie snakepipes finish finish workflow. It keeps the callOpenChromatin stage tied to upstream `filterCoveragePerScaffolds` and the downstream handoff to `tempChromSizes`. It tracks completion via `results/finish/callOpenChromatin.done`.
metadata:
  workflow_id: maxplanck-ie-snakepipes-finish
  workflow_name: maxplanck ie snakepipes finish
  step_id: callOpenChromatin
  step_name: callOpenChromatin
---

# Scope
Use this skill only for the `callOpenChromatin` step in `maxplanck-ie-snakepipes-finish`.

## Orchestration
- Upstream requirements: `filterCoveragePerScaffolds`
- Step file: `finish/maxplanck-ie-snakepipes-finish/steps/callOpenChromatin.smk`
- Config file: `finish/maxplanck-ie-snakepipes-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/callOpenChromatin.done`
- Representative outputs: `results/finish/callOpenChromatin.done`
- Execution targets: `callOpenChromatin`
- Downstream handoff: `tempChromSizes`

## Guardrails
- Treat `results/finish/callOpenChromatin.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/callOpenChromatin.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `tempChromSizes` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/callOpenChromatin.done` exists and `tempChromSizes` can proceed without re-running callOpenChromatin.
