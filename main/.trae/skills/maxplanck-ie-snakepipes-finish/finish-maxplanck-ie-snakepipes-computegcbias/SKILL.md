---
name: finish-maxplanck-ie-snakepipes-computegcbias
description: Use this skill when orchestrating the retained "computeGCBias" step of the maxplanck ie snakepipes finish finish workflow. It keeps the computeGCBias stage tied to upstream `estimate_read_filtering` and the downstream handoff to `bamPE_fragment_size`. It tracks completion via `results/finish/computeGCBias.done`.
metadata:
  workflow_id: maxplanck-ie-snakepipes-finish
  workflow_name: maxplanck ie snakepipes finish
  step_id: computeGCBias
  step_name: computeGCBias
---

# Scope
Use this skill only for the `computeGCBias` step in `maxplanck-ie-snakepipes-finish`.

## Orchestration
- Upstream requirements: `estimate_read_filtering`
- Step file: `finish/maxplanck-ie-snakepipes-finish/steps/computeGCBias.smk`
- Config file: `finish/maxplanck-ie-snakepipes-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/computeGCBias.done`
- Representative outputs: `results/finish/computeGCBias.done`
- Execution targets: `computeGCBias`
- Downstream handoff: `bamPE_fragment_size`

## Guardrails
- Treat `results/finish/computeGCBias.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/computeGCBias.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `bamPE_fragment_size` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/computeGCBias.done` exists and `bamPE_fragment_size` can proceed without re-running computeGCBias.
