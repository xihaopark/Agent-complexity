---
name: finish-maxplanck-ie-snakepipes-bamcoverage
description: Use this skill when orchestrating the retained "bamCoverage" step of the maxplanck ie snakepipes finish finish workflow. It keeps the bamCoverage stage tied to upstream `sambamba_flagstat` and the downstream handoff to `bamCoverage_filtered`. It tracks completion via `results/finish/bamCoverage.done`.
metadata:
  workflow_id: maxplanck-ie-snakepipes-finish
  workflow_name: maxplanck ie snakepipes finish
  step_id: bamCoverage
  step_name: bamCoverage
---

# Scope
Use this skill only for the `bamCoverage` step in `maxplanck-ie-snakepipes-finish`.

## Orchestration
- Upstream requirements: `sambamba_flagstat`
- Step file: `finish/maxplanck-ie-snakepipes-finish/steps/bamCoverage.smk`
- Config file: `finish/maxplanck-ie-snakepipes-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/bamCoverage.done`
- Representative outputs: `results/finish/bamCoverage.done`
- Execution targets: `bamCoverage`
- Downstream handoff: `bamCoverage_filtered`

## Guardrails
- Treat `results/finish/bamCoverage.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/bamCoverage.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `bamCoverage_filtered` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/bamCoverage.done` exists and `bamCoverage_filtered` can proceed without re-running bamCoverage.
