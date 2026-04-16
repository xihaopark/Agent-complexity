---
name: finish-maxplanck-ie-snakepipes-estimate_read_filtering
description: Use this skill when orchestrating the retained "estimate_read_filtering" step of the maxplanck ie snakepipes finish finish workflow. It keeps the estimate read filtering stage tied to upstream `plotPCA` and the downstream handoff to `computeGCBias`. It tracks completion via `results/finish/estimate_read_filtering.done`.
metadata:
  workflow_id: maxplanck-ie-snakepipes-finish
  workflow_name: maxplanck ie snakepipes finish
  step_id: estimate_read_filtering
  step_name: estimate read filtering
---

# Scope
Use this skill only for the `estimate_read_filtering` step in `maxplanck-ie-snakepipes-finish`.

## Orchestration
- Upstream requirements: `plotPCA`
- Step file: `finish/maxplanck-ie-snakepipes-finish/steps/estimate_read_filtering.smk`
- Config file: `finish/maxplanck-ie-snakepipes-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/estimate_read_filtering.done`
- Representative outputs: `results/finish/estimate_read_filtering.done`
- Execution targets: `estimate_read_filtering`
- Downstream handoff: `computeGCBias`

## Guardrails
- Treat `results/finish/estimate_read_filtering.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/estimate_read_filtering.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `computeGCBias` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/estimate_read_filtering.done` exists and `computeGCBias` can proceed without re-running estimate read filtering.
