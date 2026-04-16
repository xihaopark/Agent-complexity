---
name: finish-maxplanck-ie-snakepipes-bamcoverage_filtered
description: Use this skill when orchestrating the retained "bamCoverage_filtered" step of the maxplanck ie snakepipes finish finish workflow. It keeps the bamCoverage filtered stage tied to upstream `bamCoverage` and the downstream handoff to `plotCoverage`. It tracks completion via `results/finish/bamCoverage_filtered.done`.
metadata:
  workflow_id: maxplanck-ie-snakepipes-finish
  workflow_name: maxplanck ie snakepipes finish
  step_id: bamCoverage_filtered
  step_name: bamCoverage filtered
---

# Scope
Use this skill only for the `bamCoverage_filtered` step in `maxplanck-ie-snakepipes-finish`.

## Orchestration
- Upstream requirements: `bamCoverage`
- Step file: `finish/maxplanck-ie-snakepipes-finish/steps/bamCoverage_filtered.smk`
- Config file: `finish/maxplanck-ie-snakepipes-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/bamCoverage_filtered.done`
- Representative outputs: `results/finish/bamCoverage_filtered.done`
- Execution targets: `bamCoverage_filtered`
- Downstream handoff: `plotCoverage`

## Guardrails
- Treat `results/finish/bamCoverage_filtered.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/bamCoverage_filtered.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plotCoverage` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/bamCoverage_filtered.done` exists and `plotCoverage` can proceed without re-running bamCoverage filtered.
