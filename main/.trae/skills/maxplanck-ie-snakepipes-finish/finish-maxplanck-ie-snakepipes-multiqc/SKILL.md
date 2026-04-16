---
name: finish-maxplanck-ie-snakepipes-multiqc
description: Use this skill when orchestrating the retained "multiQC" step of the maxplanck ie snakepipes finish finish workflow. It keeps the multiQC stage tied to upstream `bamcoverage_short_cleaned` and the downstream handoff to `filterFragments`. It tracks completion via `results/finish/multiQC.done`.
metadata:
  workflow_id: maxplanck-ie-snakepipes-finish
  workflow_name: maxplanck ie snakepipes finish
  step_id: multiQC
  step_name: multiQC
---

# Scope
Use this skill only for the `multiQC` step in `maxplanck-ie-snakepipes-finish`.

## Orchestration
- Upstream requirements: `bamcoverage_short_cleaned`
- Step file: `finish/maxplanck-ie-snakepipes-finish/steps/multiQC.smk`
- Config file: `finish/maxplanck-ie-snakepipes-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/multiQC.done`
- Representative outputs: `results/finish/multiQC.done`
- Execution targets: `multiQC`
- Downstream handoff: `filterFragments`

## Guardrails
- Treat `results/finish/multiQC.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/multiQC.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `filterFragments` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/multiQC.done` exists and `filterFragments` can proceed without re-running multiQC.
