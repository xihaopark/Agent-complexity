---
name: finish-maxplanck-ie-snakepipes-tempchromsizes
description: Use this skill when orchestrating the retained "tempChromSizes" step of the maxplanck ie snakepipes finish finish workflow. It keeps the tempChromSizes stage tied to upstream `callOpenChromatin` and the downstream handoff to `HMMRATAC_peaks`. It tracks completion via `results/finish/tempChromSizes.done`.
metadata:
  workflow_id: maxplanck-ie-snakepipes-finish
  workflow_name: maxplanck ie snakepipes finish
  step_id: tempChromSizes
  step_name: tempChromSizes
---

# Scope
Use this skill only for the `tempChromSizes` step in `maxplanck-ie-snakepipes-finish`.

## Orchestration
- Upstream requirements: `callOpenChromatin`
- Step file: `finish/maxplanck-ie-snakepipes-finish/steps/tempChromSizes.smk`
- Config file: `finish/maxplanck-ie-snakepipes-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/tempChromSizes.done`
- Representative outputs: `results/finish/tempChromSizes.done`
- Execution targets: `tempChromSizes`
- Downstream handoff: `HMMRATAC_peaks`

## Guardrails
- Treat `results/finish/tempChromSizes.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/tempChromSizes.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `HMMRATAC_peaks` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/tempChromSizes.done` exists and `HMMRATAC_peaks` can proceed without re-running tempChromSizes.
